"""
로깅 유틸리티
애플리케이션의 로깅 설정 및 관리
"""

import os
import sys
from datetime import datetime
from loguru import logger
from typing import Optional


def setup_logger(log_level: str = "INFO", log_file: Optional[str] = None) -> object:
    """
    로거 설정
    
    Args:
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 로그 파일 경로 (None이면 파일 로깅 안함)
        
    Returns:
        설정된 logger 객체
    """
    # 기존 핸들러 제거
    logger.remove()
    
    # 콘솔 출력 포맷
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # 파일 출력 포맷
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} - "
        "{message}"
    )
    
    # 콘솔 핸들러 추가
    logger.add(
        sys.stderr,
        format=console_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # 파일 핸들러 추가 (선택적)
    if log_file:
        # 로그 디렉토리 생성
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logger.add(
            log_file,
            format=file_format,
            level=log_level,
            rotation="10 MB",  # 10MB마다 로테이션
            retention="1 month",  # 1개월 보관
            compression="zip",  # 압축 저장
            backtrace=True,
            diagnose=True
        )
    
    # 기본 로그 파일 설정 (logs 디렉토리)
    default_log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    if not os.path.exists(default_log_dir):
        os.makedirs(default_log_dir)
        
    default_log_file = os.path.join(
        default_log_dir,
        f"document_translator_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    logger.add(
        default_log_file,
        format=file_format,
        level="DEBUG",  # 파일에는 모든 로그 저장
        rotation="1 day",  # 하루마다 로테이션
        retention="30 days",  # 30일 보관
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    return logger


class TranslationLogger:
    """번역 작업 전용 로거"""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or datetime.now().strftime('%Y%m%d_%H%M%S')
        self.logger = setup_logger()
        
        # 번역 세션 전용 로그 파일
        session_log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "logs", 
            "sessions"
        )
        if not os.path.exists(session_log_dir):
            os.makedirs(session_log_dir)
            
        session_log_file = os.path.join(session_log_dir, f"translation_{self.session_id}.log")
        
        # 세션 전용 핸들러 추가
        self.logger.add(
            session_log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            filter=lambda record: record["extra"].get("session_id") == self.session_id
        )
        
    def log_translation_start(self, files: list, settings: dict):
        """번역 시작 로그"""
        self.logger.bind(session_id=self.session_id).info(
            f"번역 세션 시작 - 파일 수: {len(files)}, 설정: {settings}"
        )
        
    def log_file_start(self, filename: str):
        """파일 번역 시작 로그"""
        self.logger.bind(session_id=self.session_id).info(f"파일 번역 시작: {filename}")
        
    def log_file_success(self, filename: str, output_path: str):
        """파일 번역 성공 로그"""
        self.logger.bind(session_id=self.session_id).info(
            f"파일 번역 완료: {filename} → {output_path}"
        )
        
    def log_file_error(self, filename: str, error: str):
        """파일 번역 실패 로그"""
        self.logger.bind(session_id=self.session_id).error(
            f"파일 번역 실패: {filename} - {error}"
        )
        
    def log_translation_complete(self, success_count: int, total_count: int):
        """번역 완료 로그"""
        self.logger.bind(session_id=self.session_id).info(
            f"번역 세션 완료 - 성공: {success_count}/{total_count}"
        )


def get_log_files() -> list:
    """생성된 로그 파일 목록 반환"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    
    if not os.path.exists(log_dir):
        return []
        
    log_files = []
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file.endswith(('.log', '.log.zip')):
                log_files.append(os.path.join(root, file))
                
    return sorted(log_files, key=os.path.getmtime, reverse=True)


def clear_old_logs(days: int = 30):
    """오래된 로그 파일 정리"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    
    if not os.path.exists(log_dir):
        return
        
    cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
    
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_time:
                try:
                    os.remove(file_path)
                    logger.info(f"오래된 로그 파일 삭제: {file_path}")
                except Exception as e:
                    logger.warning(f"로그 파일 삭제 실패: {file_path} - {e}")


# 전역 로거 인스턴스
app_logger = setup_logger()


if __name__ == "__main__":
    # 테스트 코드
    test_logger = setup_logger("DEBUG")
    
    test_logger.debug("디버그 메시지")
    test_logger.info("정보 메시지")
    test_logger.warning("경고 메시지")
    test_logger.error("오류 메시지")
    
    # 번역 로거 테스트
    translation_logger = TranslationLogger("test_session")
    translation_logger.log_translation_start(
        ["test1.docx", "test2.xlsx"], 
        {"source": "ko", "target": "en"}
    )
    translation_logger.log_file_success("test1.docx", "output/test1_en.docx")
    translation_logger.log_translation_complete(1, 2)