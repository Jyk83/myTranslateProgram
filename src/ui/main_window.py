"""
메인 윈도우 클래스
Document Translator의 메인 GUI 인터페이스
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QLabel, QPushButton, 
                            QListWidget, QComboBox, QRadioButton, QButtonGroup,
                            QProgressBar, QTextEdit, QFileDialog, QGroupBox,
                            QGridLayout, QCheckBox, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QDragEnterEvent, QDropEvent

from ..utils.config_manager import ConfigManager
from ..utils.logger import setup_logger
from .drag_drop_widget import DragDropWidget
from .translation_worker import TranslationWorker


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.logger = setup_logger()
        self.selected_files = []
        self.translation_worker = None
        
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("Document Translator v1.0")
        self.setMinimumSize(800, 600)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 각 탭 초기화
        self.init_file_selection_tab()
        self.init_translation_settings_tab()
        self.init_output_settings_tab()
        self.init_progress_tab()
        self.init_result_tab()
        
        # 상태바
        self.statusBar().showMessage("준비 완료")
        
    def init_file_selection_tab(self):
        """파일 선택 탭 초기화"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 제목
        title = QLabel("파일 선택")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # 드래그앤드롭 영역
        self.drag_drop_widget = DragDropWidget()
        self.drag_drop_widget.files_dropped.connect(self.add_files)
        layout.addWidget(self.drag_drop_widget)
        
        # 파일 선택 버튼
        file_button_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("파일 선택")
        self.select_files_btn.clicked.connect(self.select_files)
        self.clear_files_btn = QPushButton("목록 지우기")
        self.clear_files_btn.clicked.connect(self.clear_files)
        
        file_button_layout.addWidget(self.select_files_btn)
        file_button_layout.addWidget(self.clear_files_btn)
        file_button_layout.addStretch()
        layout.addLayout(file_button_layout)
        
        # 선택된 파일 목록
        list_label = QLabel("선택된 파일:")
        layout.addWidget(list_label)
        
        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)
        
        self.tab_widget.addTab(tab, "1. 파일 선택")
        
    def init_translation_settings_tab(self):
        """번역 설정 탭 초기화"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 제목
        title = QLabel("번역 설정")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # 언어 설정 그룹
        lang_group = QGroupBox("언어 설정")
        lang_layout = QGridLayout(lang_group)
        
        # 원본 언어
        lang_layout.addWidget(QLabel("원본 언어:"), 0, 0)
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems([
            "자동 감지", "한국어", "English", "日本語", "中文", "Español", "Français"
        ])
        lang_layout.addWidget(self.source_lang_combo, 0, 1)
        
        # 목표 언어
        lang_layout.addWidget(QLabel("목표 언어:"), 1, 0)
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems([
            "한국어", "English", "日本語", "中文", "Español", "Français"
        ])
        lang_layout.addWidget(self.target_lang_combo, 1, 1)
        
        layout.addWidget(lang_group)
        
        # 전문 분야 설정 그룹
        specialty_group = QGroupBox("전문 분야")
        specialty_layout = QVBoxLayout(specialty_group)
        
        self.specialty_group = QButtonGroup()
        
        self.general_radio = QRadioButton("일반 문서")
        self.general_radio.setChecked(True)
        self.specialty_group.addButton(self.general_radio, 0)
        specialty_layout.addWidget(self.general_radio)
        
        self.art_radio = QRadioButton("예술/문화 (창의적 표현 중시)")
        self.specialty_group.addButton(self.art_radio, 1)
        specialty_layout.addWidget(self.art_radio)
        
        self.tech_radio = QRadioButton("기술/프로그래밍 (전문 용어 정확성)")
        self.specialty_group.addButton(self.tech_radio, 2)
        specialty_layout.addWidget(self.tech_radio)
        
        self.sport_radio = QRadioButton("스포츠 (관용구 및 전문 용어)")
        self.specialty_group.addButton(self.sport_radio, 3)
        specialty_layout.addWidget(self.sport_radio)
        
        layout.addWidget(specialty_group)
        
        # API 설정 그룹
        api_group = QGroupBox("번역 API")
        api_layout = QVBoxLayout(api_group)
        
        self.api_combo = QComboBox()
        self.api_combo.addItems(["OpenAI GPT-4", "Google Translate"])
        api_layout.addWidget(self.api_combo)
        
        layout.addWidget(api_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "2. 번역 설정")
        
    def init_output_settings_tab(self):
        """출력 설정 탭 초기화"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 제목
        title = QLabel("출력 설정")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # 출력 포맷 그룹
        format_group = QGroupBox("출력 포맷")
        format_layout = QVBoxLayout(format_group)
        
        self.format_group = QButtonGroup()
        
        self.original_format_radio = QRadioButton("원본 포맷 유지")
        self.original_format_radio.setChecked(True)
        self.format_group.addButton(self.original_format_radio, 0)
        format_layout.addWidget(self.original_format_radio)
        
        self.pdf_format_radio = QRadioButton("PDF 변환")
        self.format_group.addButton(self.pdf_format_radio, 1)
        format_layout.addWidget(self.pdf_format_radio)
        
        self.excel_format_radio = QRadioButton("Excel로 통합")
        self.format_group.addButton(self.excel_format_radio, 2)
        format_layout.addWidget(self.excel_format_radio)
        
        self.word_format_radio = QRadioButton("Word로 통합")
        self.format_group.addButton(self.word_format_radio, 3)
        format_layout.addWidget(self.word_format_radio)
        
        layout.addWidget(format_group)
        
        # 파일명 규칙 그룹
        naming_group = QGroupBox("파일명 규칙")
        naming_layout = QVBoxLayout(naming_group)
        
        self.naming_line_edit = QLineEdit("[원본명]_translated_[언어코드]")
        naming_layout.addWidget(self.naming_line_edit)
        
        naming_info = QLabel("사용 가능한 변수: [원본명], [언어코드], [날짜], [시간]")
        naming_info.setStyleSheet("color: gray; font-size: 10px;")
        naming_layout.addWidget(naming_info)
        
        layout.addWidget(naming_group)
        
        # 저장 경로 그룹
        path_group = QGroupBox("저장 경로")
        path_layout = QHBoxLayout(path_group)
        
        self.output_path_line_edit = QLineEdit("./output")
        path_layout.addWidget(self.output_path_line_edit)
        
        self.browse_output_btn = QPushButton("찾아보기")
        self.browse_output_btn.clicked.connect(self.browse_output_directory)
        path_layout.addWidget(self.browse_output_btn)
        
        layout.addWidget(path_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "3. 출력 설정")
        
    def init_progress_tab(self):
        """진행 상황 탭 초기화"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 제목
        title = QLabel("번역 진행")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # 진행률 표시
        progress_group = QGroupBox("진행 상태")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        self.current_file_label = QLabel("현재 처리 중인 파일: -")
        progress_layout.addWidget(self.current_file_label)
        
        layout.addWidget(progress_group)
        
        # 로그 출력
        log_group = QGroupBox("로그")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        log_layout.addWidget(self.log_text_edit)
        
        layout.addWidget(log_group)
        
        # 버튼
        button_layout = QHBoxLayout()
        self.start_translation_btn = QPushButton("번역 시작")
        self.start_translation_btn.clicked.connect(self.start_translation)
        
        self.cancel_translation_btn = QPushButton("취소")
        self.cancel_translation_btn.clicked.connect(self.cancel_translation)
        self.cancel_translation_btn.setEnabled(False)
        
        button_layout.addWidget(self.start_translation_btn)
        button_layout.addWidget(self.cancel_translation_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(tab, "4. 번역 진행")
        
    def init_result_tab(self):
        """결과 확인 탭 초기화"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 제목
        title = QLabel("번역 결과")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # 결과 파일 목록
        result_group = QGroupBox("번역 완료 파일")
        result_layout = QVBoxLayout(result_group)
        
        self.result_list_widget = QListWidget()
        result_layout.addWidget(self.result_list_widget)
        
        layout.addWidget(result_group)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        self.open_folder_btn = QPushButton("폴더 열기")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        
        self.new_translation_btn = QPushButton("새 번역 시작")
        self.new_translation_btn.clicked.connect(self.new_translation)
        
        button_layout.addWidget(self.open_folder_btn)
        button_layout.addWidget(self.new_translation_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "5. 결과 확인")
        
    def select_files(self):
        """파일 선택 대화상자"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "번역할 파일 선택",
            "",
            "지원 파일 (*.xlsx *.docx *.pptx *.pdf);;Excel 파일 (*.xlsx);;Word 파일 (*.docx);;PowerPoint 파일 (*.pptx);;PDF 파일 (*.pdf)"
        )
        if files:
            self.add_files(files)
            
    def add_files(self, file_paths):
        """파일 목록에 파일 추가"""
        for file_path in file_paths:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self.file_list_widget.addItem(os.path.basename(file_path))
        self.update_status()
        
    def clear_files(self):
        """파일 목록 지우기"""
        self.selected_files.clear()
        self.file_list_widget.clear()
        self.update_status()
        
    def browse_output_directory(self):
        """출력 디렉토리 선택"""
        directory = QFileDialog.getExistingDirectory(self, "출력 폴더 선택")
        if directory:
            self.output_path_line_edit.setText(directory)
            
    def start_translation(self):
        """번역 시작"""
        if not self.selected_files:
            QMessageBox.warning(self, "경고", "번역할 파일을 선택해주세요.")
            return
            
        # 설정 수집
        translation_settings = self.get_translation_settings()
        
        # 번역 작업자 생성 및 시작
        self.translation_worker = TranslationWorker(
            files=self.selected_files,
            settings=translation_settings
        )
        
        # 시그널 연결
        self.translation_worker.progress_updated.connect(self.update_progress)
        self.translation_worker.log_message.connect(self.add_log_message)
        self.translation_worker.file_completed.connect(self.file_translation_completed)
        self.translation_worker.translation_finished.connect(self.translation_finished)
        
        # UI 상태 변경
        self.start_translation_btn.setEnabled(False)
        self.cancel_translation_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_text_edit.clear()
        
        # 진행 탭으로 이동
        self.tab_widget.setCurrentIndex(3)
        
        # 번역 시작
        self.translation_worker.start()
        
    def cancel_translation(self):
        """번역 취소"""
        if self.translation_worker:
            self.translation_worker.stop()
            self.add_log_message("번역이 취소되었습니다.")
            self.reset_ui_state()
            
    def get_translation_settings(self):
        """현재 번역 설정 반환"""
        return {
            'source_language': self.source_lang_combo.currentText(),
            'target_language': self.target_lang_combo.currentText(),
            'specialization': self.get_selected_specialization(),
            'api_provider': self.api_combo.currentText(),
            'output_format': self.get_selected_output_format(),
            'naming_rule': self.naming_line_edit.text(),
            'output_directory': self.output_path_line_edit.text()
        }
        
    def get_selected_specialization(self):
        """선택된 전문 분야 반환"""
        checked_id = self.specialty_group.checkedId()
        specializations = ['general', 'art', 'tech', 'sport']
        return specializations[checked_id] if checked_id >= 0 else 'general'
        
    def get_selected_output_format(self):
        """선택된 출력 형식 반환"""
        checked_id = self.format_group.checkedId()
        formats = ['original', 'pdf', 'excel', 'word']
        return formats[checked_id] if checked_id >= 0 else 'original'
        
    def update_progress(self, value, current_file=""):
        """진행률 업데이트"""
        self.progress_bar.setValue(value)
        if current_file:
            self.current_file_label.setText(f"현재 처리 중인 파일: {current_file}")
            
    def add_log_message(self, message):
        """로그 메시지 추가"""
        self.log_text_edit.append(message)
        
    def file_translation_completed(self, filename, output_path):
        """파일 번역 완료 처리"""
        self.result_list_widget.addItem(f"{filename} → {output_path}")
        
    def translation_finished(self, success_count, total_count):
        """번역 완료 처리"""
        self.reset_ui_state()
        self.tab_widget.setCurrentIndex(4)  # 결과 탭으로 이동
        
        completion_message = f"번역 완료: {success_count}/{total_count} 파일"
        self.statusBar().showMessage(completion_message)
        QMessageBox.information(self, "번역 완료", completion_message)
        
    def reset_ui_state(self):
        """UI 상태 초기화"""
        self.start_translation_btn.setEnabled(True)
        self.cancel_translation_btn.setEnabled(False)
        self.current_file_label.setText("현재 처리 중인 파일: -")
        
    def open_output_folder(self):
        """출력 폴더 열기"""
        output_path = self.output_path_line_edit.text()
        if os.path.exists(output_path):
            os.startfile(output_path)  # Windows용
        else:
            QMessageBox.warning(self, "경고", "출력 폴더가 존재하지 않습니다.")
            
    def new_translation(self):
        """새 번역 시작"""
        self.clear_files()
        self.result_list_widget.clear()
        self.log_text_edit.clear()
        self.progress_bar.setValue(0)
        self.tab_widget.setCurrentIndex(0)  # 파일 선택 탭으로 이동
        
    def update_status(self):
        """상태바 업데이트"""
        file_count = len(self.selected_files)
        self.statusBar().showMessage(f"선택된 파일: {file_count}개")
        
    def load_settings(self):
        """설정 로드"""
        # ConfigManager를 통해 저장된 설정 로드
        config = self.config_manager.get_config()
        
        # UI에 설정 적용
        if 'target_language' in config['TRANSLATION']:
            target_lang = config['TRANSLATION']['target_language']
            # ComboBox에서 해당 언어 찾아서 선택
            
    def save_settings(self):
        """현재 설정 저장"""
        settings = self.get_translation_settings()
        self.config_manager.save_user_settings(settings)
        
    def closeEvent(self, event):
        """윈도우 닫기 이벤트"""
        self.save_settings()
        if self.translation_worker and self.translation_worker.isRunning():
            reply = QMessageBox.question(
                self, 
                "번역 진행 중", 
                "번역이 진행 중입니다. 정말 종료하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.translation_worker.stop()
                self.translation_worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 설정
    app.setApplicationName("Document Translator")
    app.setApplicationVersion("1.0.0")
    
    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()