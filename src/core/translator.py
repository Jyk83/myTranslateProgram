"""
번역 API 연동 모듈
OpenAI GPT-4 및 Google Translate API를 통한 번역 기능
"""

import os
import time
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# OpenAI 관련
try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None

# Google Translate 관련  
try:
    from googletrans import Translator as GoogleTranslator
    import googletrans
except ImportError:
    googletrans = None

try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None

from ..utils.logger import setup_logger
from .document_parser import DocumentContent


@dataclass
class TranslationResult:
    """번역 결과 클래스"""
    success: bool
    translated_text: str = ""
    error_message: str = ""
    original_text: str = ""
    confidence: float = 0.0


class BaseTranslator:
    """번역기 기본 클래스"""
    
    def __init__(self):
        self.logger = setup_logger()
        
    def translate(self, text: str, source_lang: str, target_lang: str, context: str = "") -> TranslationResult:
        """텍스트 번역 (하위 클래스에서 구현)"""
        raise NotImplementedError
        
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str, context: str = "") -> List[TranslationResult]:
        """배치 번역 (기본 구현: 개별 번역)"""
        results = []
        for text in texts:
            result = self.translate(text, source_lang, target_lang, context)
            results.append(result)
            time.sleep(0.1)  # API 호출 제한 방지
        return results


class OpenAITranslator(BaseTranslator):
    """OpenAI GPT-4 번역기"""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        
        if not openai:
            raise ImportError("OpenAI 라이브러리가 설치되지 않았습니다: pip install openai")
            
        # API 키 설정
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
            
        self.client = OpenAI(api_key=self.api_key)
        
        # 언어 코드 매핑
        self.language_map = {
            '자동 감지': 'auto',
            '한국어': 'Korean',
            'English': 'English', 
            '日本語': 'Japanese',
            '中文': 'Chinese',
            'Español': 'Spanish',
            'Français': 'French'
        }
        
        # 전문 분야별 프롬프트
        self.specialization_prompts = {
            'general': "다음 텍스트를 자연스럽고 정확하게 {target_lang}로 번역해주세요:",
            'art': "다음은 예술 관련 텍스트입니다. 창의적이고 감성적인 표현을 살려 {target_lang}로 번역해주세요:",
            'tech': "다음은 기술 문서입니다. 전문 용어의 정확성을 최우선으로 하여 {target_lang}로 번역해주세요. 필요시 원어를 병기해주세요:",
            'sport': "다음은 스포츠 관련 텍스트입니다. 전문 용어와 관용구를 적절히 살려 {target_lang}로 번역해주세요:"
        }
        
    def translate(self, text: str, source_lang: str, target_lang: str, context: str = "") -> TranslationResult:
        """개별 텍스트 번역"""
        try:
            if not text.strip():
                return TranslationResult(success=True, translated_text="", original_text=text)
                
            # 언어 매핑
            target_language = self.language_map.get(target_lang, target_lang)
            
            # 컨텍스트에 따른 프롬프트 선택
            specialization = context if context in self.specialization_prompts else 'general'
            prompt_template = self.specialization_prompts[specialization]
            
            # 시스템 프롬프트 구성
            system_prompt = f"""당신은 전문 번역가입니다. 다음 지침을 따라 번역해주세요:
1. 원문의 의미와 뉘앙스를 정확히 전달하세요
2. 문맥에 맞는 자연스러운 표현을 사용하세요
3. 전문 용어는 해당 분야의 표준 번역을 사용하세요
4. 번역 결과만 출력하고 부가 설명은 하지 마세요"""
            
            user_prompt = prompt_template.format(target_lang=target_language) + f"\n\n원문: {text}"
            
            # OpenAI API 호출
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # 결과 후처리
            translated_text = self._post_process_translation(translated_text, text)
            
            return TranslationResult(
                success=True,
                translated_text=translated_text,
                original_text=text,
                confidence=0.9  # GPT-4는 일반적으로 높은 품질
            )
            
        except Exception as e:
            error_msg = f"OpenAI 번역 오류: {str(e)}"
            self.logger.error(error_msg)
            return TranslationResult(
                success=False,
                error_message=error_msg,
                original_text=text
            )
            
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str, context: str = "") -> List[TranslationResult]:
        """배치 번역 (최적화된 버전)"""
        if len(texts) <= 5:
            # 적은 수의 텍스트는 하나의 요청으로 처리
            return self._translate_batch_combined(texts, source_lang, target_lang, context)
        else:
            # 많은 텍스트는 개별 처리
            return super().translate_batch(texts, source_lang, target_lang, context)
            
    def _translate_batch_combined(self, texts: List[str], source_lang: str, target_lang: str, context: str = "") -> List[TranslationResult]:
        """여러 텍스트를 하나의 요청으로 처리"""
        try:
            if not texts:
                return []
                
            # 빈 텍스트 필터링
            filtered_texts = [(i, text) for i, text in enumerate(texts) if text.strip()]
            if not filtered_texts:
                return [TranslationResult(success=True, translated_text="", original_text=text) for text in texts]
                
            target_language = self.language_map.get(target_lang, target_lang)
            specialization = context if context in self.specialization_prompts else 'general'
            
            # 배치 번역 프롬프트 구성
            system_prompt = f"""당신은 전문 번역가입니다. 여러 개의 텍스트를 {target_language}로 번역해주세요.
각 텍스트는 [번호] 형식으로 구분되어 있으며, 번역 결과도 같은 형식으로 출력해주세요.
번역 결과만 출력하고 부가 설명은 하지 마세요."""
            
            # 번호를 매겨 텍스트 구성
            numbered_texts = []
            for i, (original_idx, text) in enumerate(filtered_texts):
                numbered_texts.append(f"[{i+1}] {text}")
                
            user_prompt = f"{self.specialization_prompts[specialization].format(target_lang=target_language)}\n\n"
            user_prompt += "\n".join(numbered_texts)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            # 응답 파싱
            response_text = response.choices[0].message.content.strip()
            translated_results = self._parse_batch_response(response_text, len(filtered_texts))
            
            # 원본 순서에 맞게 결과 재구성
            results = [None] * len(texts)
            for i, (original_idx, original_text) in enumerate(filtered_texts):
                if i < len(translated_results):
                    results[original_idx] = TranslationResult(
                        success=True,
                        translated_text=translated_results[i],
                        original_text=original_text,
                        confidence=0.9
                    )
                else:
                    results[original_idx] = TranslationResult(
                        success=False,
                        error_message="배치 응답 파싱 실패",
                        original_text=original_text
                    )
                    
            # 빈 텍스트에 대한 결과 추가
            for i, text in enumerate(texts):
                if results[i] is None:
                    results[i] = TranslationResult(success=True, translated_text="", original_text=text)
                    
            return results
            
        except Exception as e:
            error_msg = f"OpenAI 배치 번역 오류: {str(e)}"
            self.logger.error(error_msg)
            return [TranslationResult(success=False, error_message=error_msg, original_text=text) for text in texts]
            
    def _parse_batch_response(self, response_text: str, expected_count: int) -> List[str]:
        """배치 응답 파싱"""
        lines = response_text.split('\n')
        results = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('[') and ']' in line:
                # [번호] 패턴 찾기
                try:
                    bracket_end = line.find(']')
                    if bracket_end > 0:
                        translated_text = line[bracket_end + 1:].strip()
                        results.append(translated_text)
                except:
                    continue
                    
        # 부족한 결과는 빈 문자열로 채우기
        while len(results) < expected_count:
            results.append("")
            
        return results[:expected_count]
        
    def _post_process_translation(self, translated_text: str, original_text: str) -> str:
        """번역 결과 후처리"""
        # 불필요한 따옴표 제거
        if translated_text.startswith('"') and translated_text.endswith('"'):
            translated_text = translated_text[1:-1]
            
        # 원문과 동일한 경우 처리
        if translated_text.lower() == original_text.lower():
            return original_text
            
        return translated_text


class GoogleTranslateAPI(BaseTranslator):
    """Google Translate API (무료 버전)"""
    
    def __init__(self):
        super().__init__()
        
        if not googletrans:
            raise ImportError("googletrans 라이브러리가 설치되지 않았습니다: pip install googletrans==3.1.0a0")
            
        self.translator = GoogleTranslator()
        
        # 언어 코드 매핑 (Google Translate 형식)
        self.language_map = {
            '자동 감지': 'auto',
            '한국어': 'ko',
            'English': 'en',
            '日本語': 'ja', 
            '中文': 'zh',
            'Español': 'es',
            'Français': 'fr'
        }
        
    def translate(self, text: str, source_lang: str, target_lang: str, context: str = "") -> TranslationResult:
        """개별 텍스트 번역"""
        try:
            if not text.strip():
                return TranslationResult(success=True, translated_text="", original_text=text)
                
            # 언어 코드 매핑
            src_code = self.language_map.get(source_lang, 'auto')
            dest_code = self.language_map.get(target_lang, 'en')
            
            # Google Translate API 호출
            result = self.translator.translate(
                text,
                src=src_code if src_code != 'auto' else None,
                dest=dest_code
            )
            
            return TranslationResult(
                success=True,
                translated_text=result.text,
                original_text=text,
                confidence=getattr(result, 'confidence', 0.8) or 0.8
            )
            
        except Exception as e:
            error_msg = f"Google Translate 오류: {str(e)}"
            self.logger.error(error_msg)
            return TranslationResult(
                success=False,
                error_message=error_msg,
                original_text=text
            )


class GoogleCloudTranslate(BaseTranslator):
    """Google Cloud Translation API (유료 버전)"""
    
    def __init__(self, credentials_path: str = None):
        super().__init__()
        
        if not translate:
            raise ImportError("google-cloud-translate 라이브러리가 설치되지 않았습니다")
            
        # 인증 설정
        credentials_path = credentials_path or os.getenv('GOOGLE_CLOUD_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
        try:
            self.client = translate.Client()
        except Exception as e:
            raise ValueError(f"Google Cloud Translation 인증 실패: {e}")
            
        # 언어 코드 매핑
        self.language_map = {
            '자동 감지': None,  # None은 자동 감지
            '한국어': 'ko',
            'English': 'en',
            '日本語': 'ja',
            '中文': 'zh',
            'Español': 'es', 
            'Français': 'fr'
        }
        
    def translate(self, text: str, source_lang: str, target_lang: str, context: str = "") -> TranslationResult:
        """개별 텍스트 번역"""
        try:
            if not text.strip():
                return TranslationResult(success=True, translated_text="", original_text=text)
                
            # 언어 코드 매핑
            src_code = self.language_map.get(source_lang)
            dest_code = self.language_map.get(target_lang, 'en')
            
            # Google Cloud Translation API 호출
            result = self.client.translate(
                text,
                source_language=src_code,
                target_language=dest_code
            )
            
            return TranslationResult(
                success=True,
                translated_text=result['translatedText'],
                original_text=text,
                confidence=0.85  # Google Cloud는 일반적으로 높은 품질
            )
            
        except Exception as e:
            error_msg = f"Google Cloud Translate 오류: {str(e)}"
            self.logger.error(error_msg)
            return TranslationResult(
                success=False,
                error_message=error_msg,
                original_text=text
            )


class TranslatorManager:
    """번역기 관리자 클래스"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.translators = {}
        self.current_translator = None
        
    def initialize_translator(self, provider: str, **kwargs) -> bool:
        """번역기 초기화"""
        try:
            if provider == "OpenAI GPT-4":
                api_key = kwargs.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
                if not api_key:
                    self.logger.error("OpenAI API 키가 설정되지 않았습니다.")
                    return False
                self.translators['openai'] = OpenAITranslator(api_key)
                self.current_translator = self.translators['openai']
                
            elif provider == "Google Translate":
                self.translators['google'] = GoogleTranslateAPI()
                self.current_translator = self.translators['google']
                
            elif provider == "Google Cloud Translate":
                credentials_path = kwargs.get('google_credentials')
                self.translators['google_cloud'] = GoogleCloudTranslate(credentials_path)
                self.current_translator = self.translators['google_cloud']
                
            else:
                self.logger.error(f"지원되지 않는 번역 제공자: {provider}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"번역기 초기화 실패 ({provider}): {e}")
            return False
            
    def translate_content(self, content: DocumentContent, source_lang: str, 
                         target_lang: str, specialization: str, provider: str) -> Optional[DocumentContent]:
        """문서 내용 번역"""
        try:
            # 번역기 초기화
            if not self.initialize_translator(provider):
                return None
                
            if not self.current_translator:
                self.logger.error("번역기가 초기화되지 않았습니다.")
                return None
                
            # 번역할 텍스트 추출
            texts_to_translate = []
            for text_block in content.text_content:
                if text_block['text'].strip():
                    texts_to_translate.append(text_block['text'])
                else:
                    texts_to_translate.append("")
                    
            if not texts_to_translate:
                self.logger.warning("번역할 텍스트가 없습니다.")
                return content
                
            # 번역 실행 (배치 또는 개별)
            self.logger.info(f"{len(texts_to_translate)}개 텍스트 번역 시작")
            
            if len(texts_to_translate) > 10:
                # 많은 텍스트는 청크로 나누어 처리
                chunk_size = 10
                all_results = []
                
                for i in range(0, len(texts_to_translate), chunk_size):
                    chunk = texts_to_translate[i:i + chunk_size]
                    chunk_results = self.current_translator.translate_batch(
                        chunk, source_lang, target_lang, specialization
                    )
                    all_results.extend(chunk_results)
                    
                    # API 제한 방지를 위한 대기
                    if i + chunk_size < len(texts_to_translate):
                        time.sleep(1)
                        
                translation_results = all_results
            else:
                translation_results = self.current_translator.translate_batch(
                    texts_to_translate, source_lang, target_lang, specialization
                )
                
            # 결과 적용
            success_count = 0
            for i, result in enumerate(translation_results):
                if i < len(content.text_content):
                    if result.success:
                        content.text_content[i]['text'] = result.translated_text
                        success_count += 1
                    else:
                        self.logger.warning(f"번역 실패 (블록 {i}): {result.error_message}")
                        
            self.logger.info(f"번역 완료: {success_count}/{len(translation_results)} 성공")
            
            return content if success_count > 0 else None
            
        except Exception as e:
            self.logger.error(f"문서 내용 번역 오류: {e}")
            return None
            
    def get_available_providers(self) -> List[str]:
        """사용 가능한 번역 제공자 목록"""
        providers = []
        
        # OpenAI 확인
        if openai and os.getenv('OPENAI_API_KEY'):
            providers.append("OpenAI GPT-4")
            
        # Google Translate 확인
        if googletrans:
            providers.append("Google Translate")
            
        # Google Cloud Translate 확인
        if translate and os.getenv('GOOGLE_CLOUD_CREDENTIALS'):
            providers.append("Google Cloud Translate")
            
        return providers
        
    def test_translator(self, provider: str) -> bool:
        """번역기 테스트"""
        try:
            if not self.initialize_translator(provider):
                return False
                
            # 간단한 테스트 번역
            test_result = self.current_translator.translate(
                "Hello, World!", "English", "한국어"
            )
            
            return test_result.success
            
        except Exception as e:
            self.logger.error(f"번역기 테스트 실패 ({provider}): {e}")
            return False