#!/usr/bin/env python3
"""
Document Translator - GUI 전용 실행 파일
표준 입력/출력 없이 GUI만 실행하는 버전
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_gui_only():
    """GUI만 실행 (콘솔 출력 최소화)"""
    try:
        # 환경 변수 로드 (선택사항)
        try:
            from dotenv import load_dotenv
            env_file = project_root / ".env"
            if env_file.exists():
                load_dotenv(env_file)
        except ImportError:
            pass
        
        # 필수 라이브러리 확인 (간단한 버전)
        try:
            import PyQt5
            from src.ui.main_window import main as run_app
        except ImportError as e:
            # GUI로 오류 표시
            try:
                from PyQt5.QtWidgets import QApplication, QMessageBox
                app = QApplication(sys.argv)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Document Translator - 오류")
                msg.setText("필수 라이브러리가 누락되었습니다")
                msg.setDetailedText(f"오류: {str(e)}\n\n해결방법:\npip install -r requirements.txt")
                msg.exec_()
                
                return 1
            except:
                # PyQt5조차 없는 경우
                print(f"PyQt5가 설치되지 않았습니다: {e}")
                return 1
        
        # GUI 애플리케이션 실행
        return run_app()
        
    except Exception as e:
        # 최후의 오류 처리
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Document Translator - 예상치 못한 오류")
            msg.setText("애플리케이션 실행 중 오류가 발생했습니다")
            msg.setDetailedText(str(e))
            msg.exec_()
            
        except:
            print(f"GUI 실행 오류: {e}")
        
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_gui_only()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(1)