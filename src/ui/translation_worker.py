"""
번역 작업자 클래스
백그라운드에서 번역 작업을 수행하는 QThread 기반 클래스
"""

import os
import traceback
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

from ..core.document_parser import DocumentParser
from ..core.translator import TranslatorManager
from ..utils.logger import setup_logger


class TranslationWorker(QThread):
    """번역 작업자 클래스"""
    
    # 시그널 정의
    progress_updated = pyqtSignal(int, str)  # 진행률, 현재 파일명
    log_message = pyqtSignal(str)  # 로그 메시지
    file_completed = pyqtSignal(str, str)  # 완료된 파일명, 출력 경로
    translation_finished = pyqtSignal(int, int)  # 성공 개수, 전체 개수
    
    def __init__(self, files, settings):
        super().__init__()
        self.files = files
        self.settings = settings
        self.is_stopped = False
        self.logger = setup_logger()
        
        # 번역기 및 파서 초기화
        self.translator_manager = TranslatorManager()
        self.document_parser = DocumentParser()
        
    def run(self):
        """메인 실행 함수"""
        try:
            self.log_message.emit("번역을 시작합니다...")
            
            total_files = len(self.files)
            success_count = 0
            
            for i, file_path in enumerate(self.files):
                if self.is_stopped:
                    self.log_message.emit("번역이 취소되었습니다.")
                    break
                    
                try:
                    # 현재 파일 처리 시작
                    filename = os.path.basename(file_path)
                    self.log_message.emit(f"처리 중: {filename}")
                    self.progress_updated.emit(int((i / total_files) * 100), filename)
                    
                    # 파일 번역 실행
                    output_path = self.translate_file(file_path)
                    
                    if output_path:
                        success_count += 1
                        self.log_message.emit(f"완료: {filename} → {os.path.basename(output_path)}")
                        self.file_completed.emit(filename, output_path)
                    else:
                        self.log_message.emit(f"실패: {filename}")
                        
                except Exception as e:
                    self.log_message.emit(f"오류 ({filename}): {str(e)}")
                    self.logger.error(f"File translation error: {e}")
                    
            # 완료 처리
            self.progress_updated.emit(100, "")
            self.translation_finished.emit(success_count, total_files)
            
        except Exception as e:
            self.log_message.emit(f"번역 중 심각한 오류가 발생했습니다: {str(e)}")
            self.logger.error(f"Translation worker error: {e}")
            
    def translate_file(self, file_path):
        """개별 파일 번역"""
        try:
            # 파일 확장자 확인
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # 문서 파싱
            self.log_message.emit(f"문서 파싱 중...")
            document_content = self.document_parser.parse_document(file_path)
            
            if not document_content:
                self.log_message.emit(f"파싱 실패: 문서에서 텍스트를 추출할 수 없습니다.")
                return None
                
            # 번역 실행
            self.log_message.emit(f"번역 중...")
            translated_content = self.translator_manager.translate_content(
                document_content,
                self.settings['source_language'],
                self.settings['target_language'],
                self.settings['specialization'],
                self.settings['api_provider']
            )
            
            if not translated_content:
                self.log_message.emit(f"번역 실패")
                return None
                
            # 결과 저장
            self.log_message.emit(f"결과 저장 중...")
            output_path = self.save_translated_document(
                file_path,
                translated_content,
                file_extension
            )
            
            return output_path
            
        except Exception as e:
            self.log_message.emit(f"파일 번역 중 오류: {str(e)}")
            self.logger.error(f"Individual file translation error: {e}")
            return None
            
    def save_translated_document(self, original_path, translated_content, file_extension):
        """번역된 문서 저장"""
        try:
            # 출력 파일명 생성
            output_filename = self.generate_output_filename(original_path)
            output_directory = self.settings['output_directory']
            
            # 출력 디렉토리 생성
            os.makedirs(output_directory, exist_ok=True)
            
            output_path = os.path.join(output_directory, output_filename)
            
            # 출력 형식에 따른 저장
            output_format = self.settings['output_format']
            
            if output_format == 'original':
                # 원본 형식 유지
                return self.document_parser.save_document(
                    translated_content, 
                    output_path, 
                    file_extension
                )
            elif output_format == 'pdf':
                # PDF로 변환
                pdf_path = os.path.splitext(output_path)[0] + '.pdf'
                return self.document_parser.save_as_pdf(translated_content, pdf_path)
            elif output_format == 'excel':
                # Excel로 통합
                excel_path = os.path.splitext(output_path)[0] + '.xlsx'
                return self.document_parser.save_as_excel(translated_content, excel_path)
            elif output_format == 'word':
                # Word로 통합
                word_path = os.path.splitext(output_path)[0] + '.docx'
                return self.document_parser.save_as_word(translated_content, word_path)
            else:
                return self.document_parser.save_document(
                    translated_content, 
                    output_path, 
                    file_extension
                )
                
        except Exception as e:
            self.log_message.emit(f"파일 저장 중 오류: {str(e)}")
            self.logger.error(f"Document saving error: {e}")
            return None
            
    def generate_output_filename(self, original_path):
        """출력 파일명 생성"""
        original_name = os.path.splitext(os.path.basename(original_path))[0]
        original_ext = os.path.splitext(original_path)[1]
        
        # 언어 코드 매핑
        lang_codes = {
            '한국어': 'ko',
            'English': 'en',
            '日本語': 'ja',
            '中文': 'zh',
            'Español': 'es',
            'Français': 'fr'
        }
        
        target_lang_code = lang_codes.get(self.settings['target_language'], 'unknown')
        
        # 파일명 규칙 적용
        naming_rule = self.settings['naming_rule']
        current_time = datetime.now()
        
        # 변수 치환
        filename = naming_rule
        filename = filename.replace('[원본명]', original_name)
        filename = filename.replace('[언어코드]', target_lang_code)
        filename = filename.replace('[날짜]', current_time.strftime('%Y%m%d'))
        filename = filename.replace('[시간]', current_time.strftime('%H%M%S'))
        
        # 출력 형식에 따른 확장자 결정
        output_format = self.settings['output_format']
        if output_format == 'pdf':
            extension = '.pdf'
        elif output_format == 'excel':
            extension = '.xlsx'
        elif output_format == 'word':
            extension = '.docx'
        else:
            extension = original_ext
            
        return filename + extension
        
    def stop(self):
        """번역 중단"""
        self.is_stopped = True
        self.log_message.emit("번역 중단 요청됨...")
        
    def get_specialization_prompt(self, specialization):
        """전문 분야에 따른 프롬프트 반환"""
        prompts = {
            'art': "다음은 예술 관련 문장입니다. 창의적이고 감성적인 표현을 살려 번역하세요:",
            'tech': "다음은 기술 문서입니다. 전문 용어는 원어 병기하고 정확성을 최우선으로 번역하세요:",
            'sport': "다음은 스포츠 관련 텍스트입니다. 전문 용어와 관용구를 적절히 번역하세요:",
            'general': "다음 문장을 자연스럽고 정확하게 번역하세요:"
        }
        return prompts.get(specialization, prompts['general'])