"""
드래그앤드롭 위젯
파일을 드래그앤드롭으로 선택할 수 있는 위젯
"""

import os
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont, QPalette


class DragDropWidget(QWidget):
    """드래그앤드롭 위젯 클래스"""
    
    files_dropped = pyqtSignal(list)  # 파일이 드롭되었을 때 시그널
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        
        # 레이아웃 설정
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # 드래그앤드롭 안내 텍스트
        self.drop_label = QLabel("파일을 여기에 드래그하세요\n\n지원 형식: .xlsx, .docx, .pptx, .pdf")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setFont(QFont("Arial", 12))
        
        layout.addWidget(self.drop_label)
        
        # 스타일 설정
        self.setStyleSheet("""
            DragDropWidget {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            DragDropWidget:hover {
                border-color: #666;
                background-color: #f0f0f0;
            }
        """)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """드래그 진입 이벤트"""
        if event.mimeData().hasUrls():
            # 드롭된 파일들 중 지원되는 형식이 있는지 확인
            valid_files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if self.is_supported_file(file_path):
                        valid_files.append(file_path)
            
            if valid_files:
                event.acceptProposedAction()
                self.setStyleSheet("""
                    DragDropWidget {
                        border: 2px dashed #4CAF50;
                        border-radius: 10px;
                        background-color: #e8f5e8;
                    }
                """)
                self.drop_label.setText("파일을 놓으세요!")
            else:
                event.ignore()
        else:
            event.ignore()
            
    def dragLeaveEvent(self, event):
        """드래그 떠남 이벤트"""
        self.reset_style()
        
    def dropEvent(self, event: QDropEvent):
        """드롭 이벤트"""
        if event.mimeData().hasUrls():
            valid_files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if self.is_supported_file(file_path):
                        valid_files.append(file_path)
            
            if valid_files:
                self.files_dropped.emit(valid_files)
                event.acceptProposedAction()
                
                # 성공 피드백
                self.setStyleSheet("""
                    DragDropWidget {
                        border: 2px solid #4CAF50;
                        border-radius: 10px;
                        background-color: #e8f5e8;
                    }
                """)
                self.drop_label.setText(f"{len(valid_files)}개 파일이 추가되었습니다!")
                
                # 2초 후 원래 스타일로 복원
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(2000, self.reset_style)
            else:
                # 지원되지 않는 파일 형식
                self.setStyleSheet("""
                    DragDropWidget {
                        border: 2px solid #f44336;
                        border-radius: 10px;
                        background-color: #ffeaea;
                    }
                """)
                self.drop_label.setText("지원되지 않는 파일 형식입니다!\n지원 형식: .xlsx, .docx, .pptx, .pdf")
                
                # 2초 후 원래 스타일로 복원
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(2000, self.reset_style)
                
    def is_supported_file(self, file_path):
        """지원되는 파일 형식인지 확인"""
        supported_extensions = ['.xlsx', '.docx', '.pptx', '.pdf']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in supported_extensions
        
    def reset_style(self):
        """스타일 초기화"""
        self.setStyleSheet("""
            DragDropWidget {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            DragDropWidget:hover {
                border-color: #666;
                background-color: #f0f0f0;
            }
        """)
        self.drop_label.setText("파일을 여기에 드래그하세요\n\n지원 형식: .xlsx, .docx, .pptx, .pdf")