#!/usr/bin/env python3
"""
Document Translator 빌드 스크립트
PyInstaller를 사용하여 실행 파일 생성
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """이전 빌드 정리"""
    print("🧹 이전 빌드 파일 정리 중...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   ✅ {dir_name} 폴더 삭제됨")
            
    # spec 파일 삭제
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   ✅ {spec_file} 삭제됨")


def check_requirements():
    """필수 요구사항 확인"""
    print("📋 빌드 요구사항 확인 중...")
    
    try:
        import PyInstaller
        print(f"   ✅ PyInstaller {PyInstaller.__version__} 설치됨")
    except ImportError:
        print("   ❌ PyInstaller가 설치되지 않았습니다.")
        print("      설치 명령: pip install pyinstaller")
        return False
        
    # 메인 파일 존재 확인
    if not os.path.exists('main.py'):
        print("   ❌ main.py 파일을 찾을 수 없습니다.")
        return False
        
    print("   ✅ main.py 파일 확인됨")
    return True


def create_icon():
    """아이콘 파일 생성 (선택사항)"""
    icon_path = "assets/icon.ico"
    
    if os.path.exists(icon_path):
        print(f"   ✅ 아이콘 파일 발견: {icon_path}")
        return icon_path
    else:
        print("   ℹ️ 아이콘 파일이 없습니다. 기본 아이콘을 사용합니다.")
        return None


def build_executable():
    """실행 파일 빌드"""
    print("🔨 실행 파일 빌드 시작...")
    
    icon_path = create_icon()
    
    # 1. 콘솔 버전 빌드
    print("📟 콘솔 버전 빌드 중...")
    cmd_console = [
        'pyinstaller',
        '--onefile',                    # 단일 실행 파일
        '--console',                    # 콘솔 창 표시
        '--name=DocumentTranslator_Console',  # 출력 파일명
        '--distpath=dist',              # 출력 디렉토리
        '--workpath=build',             # 작업 디렉토리
        '--clean',                      # 캐시 정리
    ]
    
    # 2. GUI 전용 버전 빌드
    print("🖼️ GUI 전용 버전 빌드 중...")
    cmd_gui = [
        'pyinstaller',
        '--onefile',                    # 단일 실행 파일
        '--windowed',                   # 콘솔 창 숨기기
        '--name=DocumentTranslator',    # 출력 파일명
        '--distpath=dist',              # 출력 디렉토리
        '--workpath=build',             # 작업 디렉토리
        '--clean',                      # 캐시 정리
    ]
    
    # 공통 옵션 설정
    common_options = []
    
    # 아이콘 추가 (있는 경우)
    if icon_path:
        common_options.extend(['--icon', icon_path])
    
    # 숨겨진 import 추가
    hidden_imports = [
        'openpyxl',
        'docx', 
        'pptx',
        'PyPDF2',
        'reportlab',
        'openai',
        'googletrans',
        'loguru'
    ]
    
    for module in hidden_imports:
        common_options.extend(['--hidden-import', module])
    
    # 데이터 파일 포함
    data_files = [
        ('config.ini', '.'),
        ('.env.example', '.'),
        ('README.md', '.'),
        ('docs', 'docs')
    ]
    
    for src, dest in data_files:
        if os.path.exists(src):
            common_options.extend(['--add-data', f'{src}{os.pathsep}{dest}'])
    
    # 콘솔 버전 빌드
    cmd_console.extend(common_options)
    cmd_console.append('main.py')
    
    print("콘솔 버전 빌드 명령:")
    print(" ".join(cmd_console))
    print()
    
    try:
        result = subprocess.run(cmd_console, check=True, capture_output=True, text=True)
        print("✅ 콘솔 버전 빌드 성공!")
    except subprocess.CalledProcessError as e:
        print(f"❌ 콘솔 버전 빌드 실패: {e}")
        print(f"에러 출력: {e.stderr}")
        return False
    
    # GUI 버전 빌드
    cmd_gui.extend(common_options)
    cmd_gui.append('run_gui.py')
    
    print("\nGUI 버전 빌드 명령:")
    print(" ".join(cmd_gui))
    print()
    
    try:
        result = subprocess.run(cmd_gui, check=True, capture_output=True, text=True)
        print("✅ GUI 버전 빌드 성공!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI 버전 빌드 실패: {e}")
        print(f"에러 출력: {e.stderr}")
        return False


def create_installer_data():
    """설치 관련 데이터 생성"""
    print("📦 설치 패키지 데이터 준비 중...")
    
    # 배포 폴더 구조 생성
    dist_dir = Path('dist')
    package_dir = dist_dir / 'DocumentTranslator_Package'
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    
    # 실행 파일 복사
    exe_file = dist_dir / 'DocumentTranslator.exe'
    if exe_file.exists():
        shutil.copy2(exe_file, package_dir / 'DocumentTranslator.exe')
        print("   ✅ 실행 파일 복사됨")
    
    # 문서 파일 복사
    docs_to_copy = [
        ('README.md', '사용법_README.md'),
        ('docs/USER_MANUAL.md', '사용자매뉴얼.md'),
        ('.env.example', '.env_예시파일.txt'),
        ('config.ini', 'config.ini')
    ]
    
    for src, dest in docs_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, package_dir / dest)
            print(f"   ✅ {dest} 복사됨")
    
    # 폴더 생성
    (package_dir / 'output').mkdir(exist_ok=True)
    (package_dir / 'logs').mkdir(exist_ok=True)
    (package_dir / 'config').mkdir(exist_ok=True)
    
    # 설치 안내 파일 생성
    install_guide = package_dir / '설치_및_실행방법.txt'
    install_guide.write_text("""
Document Translator 설치 및 실행 방법

=== 설치 ===
1. 이 폴더를 원하는 위치에 복사하세요.
2. .env_예시파일.txt를 참고하여 .env 파일을 생성하고 API 키를 입력하세요.

=== 실행 ===
1. DocumentTranslator.exe를 더블클릭하여 실행하세요.
2. Windows Defender 경고가 나타나면 "추가 정보" > "실행"을 클릭하세요.

=== API 키 설정 ===
1. OpenAI API 키: https://platform.openai.com 에서 발급
2. Google Translate API 키: https://console.cloud.google.com 에서 발급
3. .env 파일에 API 키를 입력하세요.

=== 문제 해결 ===
- 자세한 사용법은 "사용자매뉴얼.md" 파일을 참조하세요.
- 오류 발생시 logs 폴더의 로그 파일을 확인하세요.

문의: GitHub Issues 또는 이메일
""", encoding='utf-8')
    
    print(f"   ✅ 설치 패키지 생성됨: {package_dir}")
    
    # 압축 파일 생성
    zip_file = dist_dir / 'DocumentTranslator_v1.0_Windows'
    shutil.make_archive(str(zip_file), 'zip', package_dir)
    print(f"   ✅ 배포용 압축 파일 생성됨: {zip_file}.zip")


def verify_build():
    """빌드 결과 확인"""
    print("🔍 빌드 결과 확인 중...")
    
    gui_exe_path = Path('dist/DocumentTranslator.exe')
    console_exe_path = Path('dist/DocumentTranslator_Console.exe')
    
    success = True
    
    # GUI 버전 확인
    if gui_exe_path.exists():
        file_size = gui_exe_path.stat().st_size / (1024 * 1024)  # MB 단위
        print(f"   ✅ GUI 실행 파일 생성됨: {gui_exe_path}")
        print(f"   📏 GUI 파일 크기: {file_size:.1f} MB")
    else:
        print("   ❌ GUI 실행 파일이 생성되지 않았습니다.")
        success = False
        
    # 콘솔 버전 확인
    if console_exe_path.exists():
        file_size = console_exe_path.stat().st_size / (1024 * 1024)  # MB 단위
        print(f"   ✅ 콘솔 실행 파일 생성됨: {console_exe_path}")
        print(f"   📏 콘솔 파일 크기: {file_size:.1f} MB")
    else:
        print("   ❌ 콘솔 실행 파일이 생성되지 않았습니다.")
        success = False
        
    # 간단한 실행 테스트
    if console_exe_path.exists():
        try:
            result = subprocess.run([str(console_exe_path), '--silent'], 
                                  capture_output=True, text=True, timeout=10)
            print("   ✅ 실행 파일 테스트 성공")
        except Exception as e:
            print(f"   ⚠️ 실행 파일 테스트 실패: {e}")
        
    return success


def main():
    """메인 빌드 프로세스"""
    print("=" * 60)
    print("Document Translator 빌드 스크립트")
    print("=" * 60)
    
    try:
        # 1. 요구사항 확인
        if not check_requirements():
            return 1
            
        # 2. 이전 빌드 정리
        clean_build()
        
        # 3. 실행 파일 빌드
        if not build_executable():
            return 1
            
        # 4. 빌드 결과 확인
        if not verify_build():
            return 1
            
        # 5. 배포 패키지 생성
        create_installer_data()
        
        print("\n" + "=" * 60)
        print("🎉 빌드 완료!")
        print("📁 실행 파일: dist/DocumentTranslator.exe")
        print("📦 배포 패키지: dist/DocumentTranslator_v1.0_Windows.zip")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n빌드가 중단되었습니다.")
        return 1
    except Exception as e:
        print(f"\n❌ 빌드 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)