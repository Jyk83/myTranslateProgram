@echo off
REM Document Translator 빌드 배치 파일
REM Windows용 간편 빌드 스크립트

echo ====================================
echo Document Translator 빌드 시작
echo ====================================

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치하세요.
    pause
    exit /b 1
)

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM 의존성 설치
echo 의존성 설치 중...
pip install -r requirements.txt
if errorlevel 1 (
    echo 오류: 의존성 설치 실패
    pause
    exit /b 1
)

REM PyInstaller 설치
echo PyInstaller 설치 확인 중...
pip install pyinstaller

REM 빌드 실행
echo 빌드 실행 중...
python build.py

REM 빌드 결과 확인
if exist "dist\DocumentTranslator.exe" (
    echo.
    echo ================================
    echo 빌드 성공!
    echo 실행 파일: dist\DocumentTranslator.exe
    echo 배포 패키지: dist\DocumentTranslator_v1.0_Windows.zip
    echo ================================
    
    REM 결과 폴더 열기
    choice /M "결과 폴더를 열겠습니까"
    if errorlevel 2 goto end
    explorer dist
    
) else (
    echo.
    echo ================================
    echo 빌드 실패!
    echo 로그를 확인하세요.
    echo ================================
)

:end
pause