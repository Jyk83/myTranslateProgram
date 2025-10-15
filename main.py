#!/usr/bin/env python3
"""
Document Translator - 메인 실행 파일
Windows용 문서 번역 프로그램

사용법:
    python main.py

필수 환경 변수:
    OPENAI_API_KEY: OpenAI API 키 (선택사항)
    GOOGLE_TRANSLATE_API_KEY: Google Translate API 키 (선택사항)
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 환경 변수 로드
try:
    from dotenv import load_dotenv
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"환경변수 로드됨: {env_file}")
    else:
        print(f"환경변수 파일이 없습니다: {env_file}")
        print("API 키를 사용하려면 .env 파일을 생성하고 API 키를 설정하세요.")
except ImportError:
    print("python-dotenv가 설치되지 않았습니다. 환경변수를 직접 설정하세요.")

def safe_input(prompt="", timeout=5):
    """안전한 입력 함수 - 표준 입력이 없을 때 예외 처리"""
    try:
        # 표준 입력이 터미널에 연결되어 있는지 확인
        if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
            return input(prompt)
        else:
            # 비대화형 환경에서는 입력을 건너뜀
            print(f"{prompt}(비대화형 모드 - 자동으로 계속합니다)")
            return ""
    except (EOFError, RuntimeError, OSError):
        print(f"{prompt}(입력을 건너뜁니다)")
        return ""

def check_requirements():
    """필수 라이브러리 확인"""
    missing_libs = []
    
    try:
        import PyQt5
    except ImportError:
        missing_libs.append("PyQt5")
        
    try:
        import openpyxl
    except ImportError:
        missing_libs.append("openpyxl")
        
    try:
        import docx
    except ImportError:
        missing_libs.append("python-docx")
        
    try:
        from pptx import Presentation
    except ImportError:
        missing_libs.append("python-pptx")
        
    try:
        import PyPDF2
    except ImportError:
        missing_libs.append("PyPDF2")
        
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        missing_libs.append("reportlab")
        
    try:
        from loguru import logger
    except ImportError:
        missing_libs.append("loguru")
        
    if missing_libs:
        print("❌ 다음 라이브러리가 누락되었습니다:")
        for lib in missing_libs:
            print(f"   - {lib}")
        print("\n설치 명령:")
        print("pip install -r requirements.txt")
        return False
        
    print("✅ 모든 필수 라이브러리가 설치되어 있습니다.")
    return True

def check_api_keys():
    """API 키 확인"""
    openai_key = os.getenv('OPENAI_API_KEY')
    google_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
    
    if not openai_key and not google_key:
        print("⚠️ API 키가 설정되지 않았습니다.")
        print("OpenAI 또는 Google Translate API 키를 .env 파일에 설정하세요.")
        print("\n.env 파일 예시:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("GOOGLE_TRANSLATE_API_KEY=your_google_api_key_here")
        return False
        
    if openai_key:
        print("✅ OpenAI API 키가 설정되어 있습니다.")
    if google_key:
        print("✅ Google Translate API 키가 설정되어 있습니다.")
        
    return True

def main():
    """메인 함수"""
    # 명령행 인수 확인
    silent_mode = "--silent" in sys.argv or "--no-input" in sys.argv
    
    if not silent_mode:
        print("=" * 60)
        print("Document Translator v1.0")
        print("Windows용 다국어 문서 번역 프로그램")
        print("=" * 60)
    
    # 요구사항 확인
    if not silent_mode:
        print("\n📋 시스템 요구사항 확인 중...")
    
    if not check_requirements():
        if not silent_mode:
            safe_input("\nEnter 키를 눌러 종료하세요...")
        return 1
        
    # API 키 확인 (경고만 표시, 계속 실행)
    if not silent_mode:
        print("\n🔑 API 키 확인 중...")
        check_api_keys()
    
    # PyQt5 애플리케이션 시작
    try:
        if not silent_mode:
            print("\n🚀 애플리케이션 시작 중...")
        
        from src.ui.main_window import main as run_app
        run_app()
        
    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
        print("src 디렉토리가 올바르게 설정되어 있는지 확인하세요.")
        if not silent_mode:
            safe_input("\nEnter 키를 눌러 종료하세요...")
        return 1
        
    except Exception as e:
        print(f"❌ 애플리케이션 실행 오류: {e}")
        import traceback
        traceback.print_exc()
        if not silent_mode:
            safe_input("\nEnter 키를 눌러 종료하세요...")
        return 1
        
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        safe_input("\nEnter 키를 눌러 종료하세요...")
        sys.exit(1)