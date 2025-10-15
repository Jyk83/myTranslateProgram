# Changelog

모든 주요 변경사항이 이 파일에 문서화됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 기반으로 하며,
이 프로젝트는 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)을 따릅니다.

## [1.0.0] - 2024-01-01

### Added
- 초기 릴리즈
- Excel (.xlsx) 파일 번역 지원
- Word (.docx) 문서 번역 지원
- PowerPoint (.pptx) 프레젠테이션 번역 지원
- PDF 파일 번역 지원
- OpenAI GPT-4 API 연동
- Google Translate API 연동
- 드래그앤드롭 파일 선택 인터페이스
- 5단계 탭 기반 사용자 인터페이스
- 전문 분야별 번역 최적화
  - 일반 문서
  - 예술/문화
  - 기술/프로그래밍
  - 스포츠
- 다국어 지원 (한국어, 영어, 일본어, 중국어, 스페인어, 프랑스어)
- 여러 출력 형식 지원
  - 원본 형식 유지
  - PDF 변환
  - Excel 통합
  - Word 통합
- 배치 파일 처리
- 실시간 진행률 표시
- 상세 로깅 시스템
- 사용자 설정 저장 및 복원
- 번역 히스토리 관리
- PyInstaller 기반 실행 파일 생성
- 포괄적인 사용자 매뉴얼 및 문서

### Technical Details
- Python 3.8+ 호환
- PyQt5 기반 GUI
- 모듈형 아키텍처 설계
- 상세 에러 처리 및 복구
- 설정 파일 기반 구성 관리
- 단위 테스트 포함

### Dependencies
- PyQt5 5.15.9
- openpyxl 3.1.2
- python-docx 1.1.0
- python-pptx 0.6.23
- PyPDF2 3.0.1
- reportlab 4.0.7
- openai 1.3.7
- googletrans 3.1.0a0
- loguru 0.7.2

## [Unreleased]

### Planned Features
- 대화형 번역 미리보기
- 추가 파일 형식 지원 (.odt, .rtf)
- 번역 품질 평가 시스템
- 클라우드 스토리지 연동
- 실시간 협업 기능
- 음성 입력/출력 지원
- 자동 업데이트 시스템

### Known Issues
- 대용량 PDF 파일 처리 시 메모리 사용량 증가
- 복잡한 Excel 수식이 포함된 셀 처리 제한
- 일부 PDF의 이미지 내 텍스트 추출 불가

---

**버전 표기법**
- Major.Minor.Patch (예: 1.0.0)
- Major: 호환성을 깨는 변경사항
- Minor: 기능 추가 (하위 호환)
- Patch: 버그 수정 (하위 호환)