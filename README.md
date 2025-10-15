# 📄 Document Translator

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)

**Windows용 AI 기반 다국어 문서 번역 프로그램**

*Excel, Word, PowerPoint, PDF 파일을 고품질로 번역하는 데스크톱 애플리케이션*

[📥 다운로드](#-설치-및-실행) • [📖 사용법](#-사용-방법) • [🐛 문제 해결](#-문제-해결) • [🤝 기여](#-기여)

</div>

---

## 📋 개요

Document Translator는 **Excel, Word, PowerPoint, PDF** 문서를 다양한 언어로 번역해주는 Windows 데스크톱 애플리케이션입니다. 

🤖 **AI 기반 번역**: OpenAI GPT-4와 Google Translate API 지원  
🎯 **전문 분야별 최적화**: 일반/예술/기술/스포츠 분야별 맞춤 번역  
🖱️ **사용자 친화적**: 직관적인 드래그앤드롭 인터페이스  
⚡ **배치 처리**: 여러 파일 동시 번역 지원

## 🎬 데모

> 📸 *스크린샷 및 데모 영상은 추후 추가 예정*

### 주요 화면
- **파일 선택**: 드래그앤드롭으로 간편한 파일 선택
- **번역 설정**: 언어 및 전문 분야 선택
- **실시간 진행**: 번역 진행률과 로그 실시간 확인
- **결과 확인**: 번역 완료 파일 관리

## ✨ 주요 기능

### 📁 지원 파일 형식
- **Excel** (.xlsx) - 셀 단위 번역, 수식 제외
- **Word** (.docx) - 문단 및 표 내용 번역
- **PowerPoint** (.pptx) - 슬라이드 텍스트 번역
- **PDF** (.pdf) - 텍스트 추출 후 번역

### 🌍 지원 언어
- 한국어 (Korean)
- 영어 (English)
- 일본어 (日本語)
- 중국어 (中文)
- 스페인어 (Español)
- 프랑스어 (Français)

### 🎯 전문 분야별 번역
- **일반 문서**: 표준 번역
- **예술/문화**: 창의적 표현 중시
- **기술/프로그래밍**: 전문 용어 정확성 우선
- **스포츠**: 관용구 및 전문 용어 적절히 번역

### 📤 출력 옵션
- **원본 형식 유지**: 레이아웃과 서식 보존
- **PDF 변환**: 모든 파일을 PDF로 통합
- **Excel 통합**: 번역 결과를 Excel 표로 정리
- **Word 통합**: 하나의 Word 문서로 통합

## 🛠️ 기술 스택

### 프론트엔드
- **PyQt5**: 크로스플랫폼 GUI 프레임워크
- **Custom Widgets**: 드래그앤드롭, 진행률 표시

### 백엔드
- **Python 3.8+**: 메인 개발 언어
- **Threading**: 비동기 번역 처리
- **Logging**: 상세한 로깅 시스템

### 문서 처리
- **openpyxl**: Excel 파일 처리
- **python-docx**: Word 문서 처리
- **python-pptx**: PowerPoint 파일 처리
- **PyPDF2 + reportlab**: PDF 읽기/쓰기

### AI/번역 API
- **OpenAI GPT-4**: 고품질 AI 번역
- **Google Translate**: 빠른 기계 번역
- **Custom Prompts**: 전문 분야별 프롬프트 최적화

## ⚡ 빠른 시작

### 5분만에 시작하기

```bash
# 1. 저장소 복제
git clone https://github.com/Jyk83/myTranslateProgram.git
cd myTranslateProgram

# 2. 의존성 설치 (권장: 단계별 설치)
python install_dependencies.py

# 또는 한 번에 설치 (의존성 충돌 가능)
pip install -r requirements-minimal.txt

# 3. API 키 설정 (선택)
cp .env.example .env
# .env 파일에 OpenAI 또는 Google API 키 입력

# 4. 프로그램 실행
python main.py
```

> 💡 **팁**: API 키 없이도 데모 모드로 실행 가능합니다!

## 🚀 설치 및 실행

### 시스템 요구사항
- Windows 10/11
- Python 3.8 이상
- 최소 4GB RAM
- 100MB 이상 디스크 공간

### 설치 방법

1. **저장소 복제**
```bash
git clone https://github.com/Jyk83/myTranslateProgram.git
cd myTranslateProgram
```

2. **가상환경 생성 (권장)**
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
```

3. **의존성 설치**

**방법 1: 자동 설치 스크립트 (권장)**
```bash
python install_dependencies.py
```

**방법 2: 최소 필수 라이브러리만 설치**
```bash
pip install -r requirements-minimal.txt
```

**방법 3: 전체 라이브러리 설치 (충돌 가능)**
```bash
pip install -r requirements.txt
```

4. **API 키 설정**
`.env.example` 파일을 `.env`로 복사하고 API 키를 입력:
```bash
copy .env.example .env
```

`.env` 파일 편집:
```env
# OpenAI API 키 (GPT-4 사용시 필요)
OPENAI_API_KEY=your_openai_api_key_here

# Google Translate API 키 (Google Translate 사용시 필요)
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here

# Google Cloud Translate (고급 기능)
GOOGLE_CLOUD_CREDENTIALS=path/to/service-account-key.json
```

5. **애플리케이션 실행**
```bash
python main.py
```

## 📖 사용 방법

### 1단계: 파일 선택
- **드래그앤드롭**: 파일을 드래그앤드롭 영역에 끌어다 놓기
- **파일 선택**: "파일 선택" 버튼으로 파일 선택
- 여러 파일 동시 선택 가능

### 2단계: 번역 설정
- **원본 언어**: 자동 감지 또는 수동 선택
- **목표 언어**: 번역할 언어 선택
- **전문 분야**: 문서 유형에 맞는 전문 분야 선택
- **API 제공자**: OpenAI GPT-4 또는 Google Translate 선택

### 3단계: 출력 설정
- **출력 형식**: 원본 유지, PDF 변환, Excel/Word 통합
- **파일명 규칙**: 자동 생성 규칙 설정
- **저장 경로**: 번역 파일 저장 위치 선택

### 4단계: 번역 실행
- "번역 시작" 버튼 클릭
- 진행률 및 로그 실시간 확인
- 필요시 "취소" 버튼으로 중단

### 5단계: 결과 확인
- 번역 완료 파일 목록 확인
- "폴더 열기"로 결과 파일 위치 확인
- "새 번역 시작"으로 새로운 번역 작업 시작

## 🛠️ API 키 획득 방법

### OpenAI API 키
1. [OpenAI 계정 생성](https://platform.openai.com)
2. API Keys 메뉴에서 새 키 생성
3. 요금제 확인 및 결제 정보 등록

### Google Translate API 키
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. Cloud Translation API 활성화
4. 자격 증명 > API 키 생성

## ⚙️ 고급 설정

### 설정 파일 위치
- **메인 설정**: `config.ini`
- **사용자 설정**: `config/user_settings.json`
- **번역 히스토리**: `config/translation_history.json`
- **API 키**: `config/api_keys.json`

### 로그 파일
- **메인 로그**: `logs/document_translator_YYYYMMDD.log`
- **세션 로그**: `logs/sessions/translation_YYYYMMDD_HHMMSS.log`

### 환경 변수
```env
# OpenAI 설정
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4                    # 기본: gpt-4

# Google 설정  
GOOGLE_TRANSLATE_API_KEY=your_key
GOOGLE_CLOUD_CREDENTIALS=path/to/json

# 애플리케이션 설정
LOG_LEVEL=INFO                        # DEBUG, INFO, WARNING, ERROR
MAX_FILE_SIZE_MB=50                   # 최대 파일 크기
```

## 📦 실행 파일 생성

PyInstaller를 사용하여 독립 실행 파일 생성:

```bash
# 개발 빌드
python -m PyInstaller --onefile --windowed main.py

# 최적화 빌드 (build.py 사용)
python build.py
```

생성된 실행 파일: `dist/main.exe`

## 🐛 문제 해결

### 자주 발생하는 문제

**Q: "ModuleNotFoundError" 또는 의존성 충돌 오류가 발생합니다**
A: 다음 방법들을 순서대로 시도하세요:
```bash
# 방법 1: 자동 설치 스크립트 사용
python install_dependencies.py

# 방법 2: 최소 라이브러리만 설치
pip install -r requirements-minimal.txt

# 방법 3: 가상환경 새로 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements-minimal.txt
```

**Q: API 키 오류가 발생합니다**
A: `.env` 파일의 API 키가 올바른지 확인하고, 계정에 잔액이 있는지 확인하세요.

**Q: 특정 파일이 번역되지 않습니다**
A: 파일이 손상되었거나 암호로 보호되어 있는지 확인하세요. 로그에서 상세 오류를 확인할 수 있습니다.

**Q: 번역 품질이 좋지 않습니다**
A: 전문 분야 설정을 확인하고, OpenAI GPT-4 사용을 권장합니다.

**Q: 프로그램이 느려집니다**
A: 대용량 파일이나 많은 파일을 한 번에 처리할 때 발생할 수 있습니다. 파일을 나누어 처리하세요.

### 로그 확인
상세한 오류 정보는 `logs` 폴더의 로그 파일에서 확인할 수 있습니다.

## 🔒 보안 및 개인정보

- API 키는 로컬에만 저장됩니다
- 번역 내용은 선택한 API 제공자의 정책을 따릅니다
- 로그 파일에는 개인정보가 포함될 수 있으므로 주의하세요

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📁 프로젝트 구조

```
myTranslateProgram/
├── 📄 main.py                 # 메인 실행 파일
├── 📋 requirements.txt        # 의존성 목록
├── ⚙️ config.ini             # 애플리케이션 설정
├── 🔐 .env.example           # API 키 설정 템플릿
├── 📖 README.md              # 프로젝트 문서
├── 📜 LICENSE                # MIT 라이선스
├── 🔨 build.py               # 실행 파일 빌드
├── 📂 src/
│   ├── 🖥️ ui/                # GUI 인터페이스
│   ├── ⚡ core/              # 핵심 로직
│   └── 🛠️ utils/             # 유틸리티
├── 📚 docs/                  # 문서
├── 🧪 tests/                 # 단위 테스트
└── 📦 assets/                # 리소스
```

## 🤝 기여하기

모든 기여를 환영합니다! 🎉

### 기여 방법
1. **🍴 Fork** 저장소
2. **🌿 브랜치 생성**: `git checkout -b feature/amazing-feature`
3. **💾 변경사항 커밋**: `git commit -m 'feat: Add amazing feature'`
4. **📤 브랜치 푸시**: `git push origin feature/amazing-feature`
5. **🔄 Pull Request 생성**

### 개발 환경 설정
```bash
# 개발 모드로 설치
pip install -e .
pip install -r requirements-dev.txt

# 테스트 실행
python run_tests.py

# 코드 품질 검사
flake8 src/
black src/
```

### 기여 가이드라인
- 🧪 새로운 기능에는 테스트 추가
- 📝 변경사항 문서화
- 💬 명확한 커밋 메시지 사용
- 🎯 한 번에 하나의 기능만 구현

## 📞 지원

- **이슈 트래커**: [GitHub Issues](https://github.com/Jyk83/myTranslateProgram/issues)
- **문의**: GitHub Issues를 통해 문의해주세요
- **문서**: 내장된 사용자 매뉴얼 참조

## 📝 변경 로그

### v1.0.0 (2024-10-15)
- 🎉 초기 릴리즈
- 📄 Excel, Word, PowerPoint, PDF 지원
- 🤖 OpenAI GPT-4, Google Translate 지원
- 🖱️ 드래그앤드롭 인터페이스
- 🎯 전문 분야별 번역
- ⚡ 배치 처리 기능

## 🗺️ 로드맵

### v1.1.0 (계획중)
- [ ] 🖼️ 실시간 번역 미리보기
- [ ] 📊 번역 품질 평가 시스템
- [ ] 🔄 번역 결과 비교 기능
- [ ] 🎨 다크 테마 지원

### v1.2.0 (계획중)
- [ ] ☁️ 클라우드 스토리지 연동 (Google Drive, OneDrive)
- [ ] 🌐 웹 기반 관리 대시보드
- [ ] 👥 팀 협업 기능
- [ ] 📱 모바일 앱 연동

### 장기 계획
- [ ] 🎤 음성 입력/출력 지원
- [ ] 🔄 자동 업데이트 시스템
- [ ] 🌍 더 많은 언어 지원
- [ ] 🤝 오픈소스 번역 모델 연동

## 💝 감사 인사

이 프로젝트는 다음 오픈소스 프로젝트들 덕분에 가능했습니다:

- **PyQt5**: 강력한 GUI 프레임워크
- **OpenAI**: 뛰어난 AI 번역 모델
- **Google Translate**: 신뢰할 수 있는 번역 서비스
- **Python 커뮤니티**: 훌륭한 라이브러리 생태계

특별히 문서 처리 라이브러리 개발자들께 감사드립니다:
`openpyxl`, `python-docx`, `python-pptx`, `PyPDF2`, `reportlab`

## ⭐ 지원하기

이 프로젝트가 도움이 되셨다면:
- ⭐ **Star**를 눌러주세요
- 🐛 **버그 리포트** 또는 💡 **기능 제안**을 해주세요
- 📢 **친구들에게 공유**해주세요
- 🤝 **기여**해주세요

---

<div align="center">

**🚀 Document Translator - 문서 번역의 새로운 경험을 제공합니다 🚀**

*Made with ❤️ for the global community*

[![GitHub stars](https://img.shields.io/github/stars/Jyk83/myTranslateProgram?style=social)](https://github.com/Jyk83/myTranslateProgram/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Jyk83/myTranslateProgram?style=social)](https://github.com/Jyk83/myTranslateProgram/network)

</div>