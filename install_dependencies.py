#!/usr/bin/env python3
"""
Document Translator 의존성 설치 스크립트
라이브러리 충돌을 방지하면서 단계별로 설치
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """명령어 실행 및 결과 확인"""
    print(f"🔄 {description}")
    print(f"실행: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 성공!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 실패: {e}")
        if e.stdout:
            print(f"출력: {e.stdout}")
        if e.stderr:
            print(f"오류: {e.stderr}")
        return False

def install_step_by_step():
    """단계별 라이브러리 설치"""
    print("=" * 60)
    print("Document Translator 의존성 설치")
    print("=" * 60)
    
    # 1단계: pip 업그레이드
    print("\n📦 1단계: pip 업그레이드")
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                       "pip 최신 버전으로 업그레이드"):
        return False
    
    # 2단계: 핵심 GUI 라이브러리
    print("\n🖥️ 2단계: GUI 프레임워크 설치")
    gui_packages = ["PyQt5"]
    for package in gui_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"{package} 설치"):
            return False
    
    # 3단계: 문서 처리 라이브러리
    print("\n📄 3단계: 문서 처리 라이브러리 설치")
    doc_packages = ["openpyxl", "python-docx", "python-pptx", "PyPDF2", "reportlab"]
    for package in doc_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"{package} 설치"):
            return False
    
    # 4단계: 번역 라이브러리 (충돌 방지)
    print("\n🌍 4단계: 번역 라이브러리 설치")
    
    # OpenAI 먼저 설치
    if not run_command([sys.executable, "-m", "pip", "install", "openai>=1.3.0"], 
                       "OpenAI 라이브러리 설치"):
        return False
    
    # deep-translator 설치 (googletrans 대신)
    if not run_command([sys.executable, "-m", "pip", "install", "deep-translator"], 
                       "Deep Translator 라이브러리 설치"):
        return False
    
    # 5단계: 유틸리티 라이브러리
    print("\n🛠️ 5단계: 유틸리티 라이브러리 설치")
    util_packages = ["requests", "python-dotenv", "loguru", "Pillow"]
    for package in util_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package], 
                          f"{package} 설치"):
            return False
    
    # 6단계: 빌드 도구 (선택사항)
    print("\n🔨 6단계: 빌드 도구 설치 (선택사항)")
    if not run_command([sys.executable, "-m", "pip", "install", "PyInstaller"], 
                       "PyInstaller 설치"):
        print("⚠️ PyInstaller 설치 실패 (빌드 기능 제외하고 계속)")
    
    print("\n" + "=" * 60)
    print("✅ 의존성 설치 완료!")
    print("=" * 60)
    return True

def verify_installation():
    """설치 확인"""
    print("\n🔍 설치 확인 중...")
    
    required_packages = [
        "PyQt5",
        "openpyxl", 
        "docx",
        "pptx",
        "PyPDF2",
        "reportlab",
        "openai",
        "deep_translator",
        "requests",
        "dotenv",
        "loguru"
    ]
    
    failed_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ 다음 패키지 설치 실패: {', '.join(failed_packages)}")
        return False
    else:
        print("\n✅ 모든 필수 패키지가 정상적으로 설치되었습니다!")
        return True

def main():
    """메인 함수"""
    try:
        # 단계별 설치
        if install_step_by_step():
            # 설치 확인
            if verify_installation():
                print("\n🎉 설치가 성공적으로 완료되었습니다!")
                print("\n다음 명령으로 프로그램을 실행할 수 있습니다:")
                print("python main.py")
                print("또는")
                print("python run_gui.py")
                return 0
            else:
                print("\n❌ 일부 패키지 설치에 문제가 있습니다.")
                return 1
        else:
            print("\n❌ 설치 중 오류가 발생했습니다.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 설치가 중단되었습니다.")
        return 1
    except Exception as e:
        print(f"\n예상치 못한 오류: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())