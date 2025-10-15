# Document Translator

Windows용 다국어 문서 번역 프로그램

## 📋 개요

Document Translator는 Excel, Word, PowerPoint, PDF 문서를 다양한 언어로 번역해주는 Windows 데스크톱 애플리케이션입니다. OpenAI GPT-4와 Google Translate API를 지원하며, 전문 분야별 맞춤 번역을 제공합니다.

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
- 원본 형식 유지
- PDF 변환
- Excel 통합 출력
- Word 통합 출력

## 🚀 설치 및 실행

### 시스템 요구사항
- Windows 10/11
- Python 3.8 이상
- 최소 4GB RAM
- 100MB 이상 디스크 공간

### 설치 방법

1. **저장소 복제**
```bash
git clone https://github.com/your-username/document-translator.git
cd document-translator
```

2. **가상환경 생성 (권장)**
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
```

3. **의존성 설치**
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

**Q: "ModuleNotFoundError" 오류가 발생합니다**
A: `pip install -r requirements.txt`로 의존성을 다시 설치하세요.

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

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

- **이슈 트래커**: [GitHub Issues](https://github.com/your-username/document-translator/issues)
- **이메일**: support@example.com
- **문서**: 내장된 사용자 매뉴얼 참조

## 📝 변경 로그

### v1.0.0 (2024-01-01)
- 초기 릴리즈
- Excel, Word, PowerPoint, PDF 지원
- OpenAI GPT-4, Google Translate 지원
- 드래그앤드롭 인터페이스
- 전문 분야별 번역
- 배치 처리 기능

---

**Document Translator** - 문서 번역의 새로운 경험을 제공합니다.