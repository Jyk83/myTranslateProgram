"""
설정 관리 모듈
애플리케이션 설정 및 사용자 기본 설정 관리
"""

import os
import json
import configparser
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from .logger import setup_logger


class ConfigManager:
    """설정 관리자 클래스"""
    
    def __init__(self, config_dir: str = None):
        self.logger = setup_logger()
        
        # 설정 디렉토리 설정
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # 기본 설정 디렉토리 (프로젝트 루트의 config 폴더)
            project_root = Path(__file__).parent.parent.parent
            self.config_dir = project_root / "config"
            
        self.config_dir.mkdir(exist_ok=True)
        
        # 설정 파일 경로
        self.main_config_file = project_root / "config.ini"
        self.user_config_file = self.config_dir / "user_settings.json"
        self.history_file = self.config_dir / "translation_history.json"
        self.api_keys_file = self.config_dir / "api_keys.json"
        
        # 기본 설정 로드
        self.config = self._load_main_config()
        self.user_settings = self._load_user_settings()
        self.history = self._load_history()
        
    def _load_main_config(self) -> configparser.ConfigParser:
        """메인 설정 파일 로드"""
        config = configparser.ConfigParser()
        
        try:
            if self.main_config_file.exists():
                config.read(self.main_config_file, encoding='utf-8')
            else:
                # 기본 설정 생성
                self._create_default_config(config)
                self._save_main_config(config)
                
        except Exception as e:
            self.logger.error(f"메인 설정 로드 실패: {e}")
            self._create_default_config(config)
            
        return config
        
    def _create_default_config(self, config: configparser.ConfigParser):
        """기본 설정 생성"""
        config['TRANSLATION'] = {
            'source_language': 'auto',
            'target_language': 'ko',
            'specialization': 'general',
            'api_provider': 'openai',
            'languages': 'ko:한국어,en:English,ja:日本語,zh:中文,es:Español,fr:Français',
            'specializations': 'general:일반 문서,art:예술/문화,tech:기술/프로그래밍,sport:스포츠'
        }
        
        config['OUTPUT'] = {
            'format': 'original',
            'naming_rule': '[원본명]_translated_[언어코드]',
            'output_directory': './output'
        }
        
        config['API'] = {
            'openai_model': 'gpt-4',
            'max_retries': '3',
            'timeout': '30'
        }
        
        config['HISTORY'] = {
            'max_history_items': '10',
            'save_history': 'true'
        }
        
        config['UI'] = {
            'window_width': '800',
            'window_height': '600',
            'theme': 'default'
        }
        
    def _save_main_config(self, config: configparser.ConfigParser):
        """메인 설정 파일 저장"""
        try:
            with open(self.main_config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            self.logger.error(f"메인 설정 저장 실패: {e}")
            
    def _load_user_settings(self) -> Dict[str, Any]:
        """사용자 설정 로드"""
        try:
            if self.user_config_file.exists():
                with open(self.user_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_user_settings()
        except Exception as e:
            self.logger.error(f"사용자 설정 로드 실패: {e}")
            return self._get_default_user_settings()
            
    def _get_default_user_settings(self) -> Dict[str, Any]:
        """기본 사용자 설정 반환"""
        return {
            'last_used': {
                'source_language': '자동 감지',
                'target_language': '한국어',
                'specialization': 'general',
                'api_provider': 'OpenAI GPT-4',
                'output_format': 'original',
                'output_directory': './output'
            },
            'preferences': {
                'auto_save_settings': True,
                'show_progress_details': True,
                'confirm_before_overwrite': True,
                'max_file_size_mb': 50
            },
            'ui_state': {
                'window_size': [800, 600],
                'window_position': [100, 100],
                'last_tab': 0
            }
        }
        
    def _save_user_settings(self):
        """사용자 설정 저장"""
        try:
            with open(self.user_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"사용자 설정 저장 실패: {e}")
            
    def _load_history(self) -> List[Dict[str, Any]]:
        """번역 히스토리 로드"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            self.logger.error(f"히스토리 로드 실패: {e}")
            return []
            
    def _save_history(self):
        """번역 히스토리 저장"""
        try:
            # 최대 개수 제한
            max_items = int(self.config.get('HISTORY', 'max_history_items', fallback=10))
            if len(self.history) > max_items:
                self.history = self.history[-max_items:]
                
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"히스토리 저장 실패: {e}")
            
    def get_config(self) -> configparser.ConfigParser:
        """메인 설정 반환"""
        return self.config
        
    def get_user_settings(self) -> Dict[str, Any]:
        """사용자 설정 반환"""
        return self.user_settings
        
    def get_last_used_settings(self) -> Dict[str, Any]:
        """마지막 사용 설정 반환"""
        return self.user_settings.get('last_used', {})
        
    def save_user_settings(self, settings: Dict[str, Any]):
        """사용자 설정 업데이트 및 저장"""
        try:
            # 마지막 사용 설정 업데이트
            if 'last_used' not in self.user_settings:
                self.user_settings['last_used'] = {}
                
            self.user_settings['last_used'].update({
                'source_language': settings.get('source_language'),
                'target_language': settings.get('target_language'),
                'specialization': settings.get('specialization'),
                'api_provider': settings.get('api_provider'),
                'output_format': settings.get('output_format'),
                'output_directory': settings.get('output_directory')
            })
            
            self._save_user_settings()
            self.logger.info("사용자 설정 저장 완료")
            
        except Exception as e:
            self.logger.error(f"사용자 설정 저장 오류: {e}")
            
    def add_to_history(self, translation_info: Dict[str, Any]):
        """번역 히스토리에 추가"""
        try:
            history_item = {
                'timestamp': datetime.now().isoformat(),
                'files': translation_info.get('files', []),
                'settings': translation_info.get('settings', {}),
                'results': translation_info.get('results', {}),
                'success_count': translation_info.get('success_count', 0),
                'total_count': translation_info.get('total_count', 0)
            }
            
            self.history.append(history_item)
            self._save_history()
            self.logger.info("번역 히스토리 추가됨")
            
        except Exception as e:
            self.logger.error(f"히스토리 추가 오류: {e}")
            
    def get_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """번역 히스토리 반환"""
        if limit:
            return self.history[-limit:]
        return self.history
        
    def clear_history(self):
        """히스토리 지우기"""
        self.history.clear()
        self._save_history()
        self.logger.info("번역 히스토리 삭제됨")
        
    def save_api_keys(self, api_keys: Dict[str, str]):
        """API 키 저장 (암호화 필요시 추가 구현)"""
        try:
            # 보안을 위해 실제 배포시에는 암호화 필요
            with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                json.dump(api_keys, f, ensure_ascii=False, indent=2)
            
            # 파일 권한 설정 (Unix 계열)
            if os.name != 'nt':
                os.chmod(self.api_keys_file, 0o600)
                
            self.logger.info("API 키 저장 완료")
            
        except Exception as e:
            self.logger.error(f"API 키 저장 실패: {e}")
            
    def load_api_keys(self) -> Dict[str, str]:
        """API 키 로드"""
        try:
            if self.api_keys_file.exists():
                with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"API 키 로드 실패: {e}")
            return {}
            
    def get_language_options(self) -> Dict[str, str]:
        """언어 옵션 반환"""
        languages_str = self.config.get('TRANSLATION', 'languages', fallback='')
        languages = {}
        
        for lang_pair in languages_str.split(','):
            if ':' in lang_pair:
                code, name = lang_pair.split(':', 1)
                languages[code.strip()] = name.strip()
                
        return languages
        
    def get_specialization_options(self) -> Dict[str, str]:
        """전문 분야 옵션 반환"""
        specializations_str = self.config.get('TRANSLATION', 'specializations', fallback='')
        specializations = {}
        
        for spec_pair in specializations_str.split(','):
            if ':' in spec_pair:
                code, name = spec_pair.split(':', 1)
                specializations[code.strip()] = name.strip()
                
        return specializations
        
    def update_ui_state(self, window_size: List[int], window_position: List[int], last_tab: int):
        """UI 상태 업데이트"""
        if 'ui_state' not in self.user_settings:
            self.user_settings['ui_state'] = {}
            
        self.user_settings['ui_state'].update({
            'window_size': window_size,
            'window_position': window_position,
            'last_tab': last_tab
        })
        
        self._save_user_settings()
        
    def get_ui_state(self) -> Dict[str, Any]:
        """UI 상태 반환"""
        return self.user_settings.get('ui_state', {
            'window_size': [800, 600],
            'window_position': [100, 100],
            'last_tab': 0
        })
        
    def export_settings(self, export_path: str) -> bool:
        """설정 내보내기"""
        try:
            export_data = {
                'user_settings': self.user_settings,
                'history': self.history,
                'export_date': datetime.now().isoformat()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"설정 내보내기 완료: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"설정 내보내기 실패: {e}")
            return False
            
    def import_settings(self, import_path: str) -> bool:
        """설정 가져오기"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            # 설정 복원
            if 'user_settings' in import_data:
                self.user_settings = import_data['user_settings']
                self._save_user_settings()
                
            if 'history' in import_data:
                self.history = import_data['history']
                self._save_history()
                
            self.logger.info(f"설정 가져오기 완료: {import_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"설정 가져오기 실패: {e}")
            return False
            
    def reset_settings(self):
        """설정 초기화"""
        try:
            # 사용자 설정 초기화
            self.user_settings = self._get_default_user_settings()
            self._save_user_settings()
            
            # 히스토리 초기화
            self.clear_history()
            
            # API 키는 유지 (선택사항)
            
            self.logger.info("설정 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"설정 초기화 실패: {e}")


# 전역 설정 관리자 인스턴스
config_manager = ConfigManager()


if __name__ == "__main__":
    # 테스트 코드
    cm = ConfigManager()
    
    print("언어 옵션:", cm.get_language_options())
    print("전문분야 옵션:", cm.get_specialization_options())
    print("마지막 사용 설정:", cm.get_last_used_settings())
    
    # 테스트 히스토리 추가
    cm.add_to_history({
        'files': ['test.docx'],
        'settings': {'source': 'ko', 'target': 'en'},
        'results': {'success': True},
        'success_count': 1,
        'total_count': 1
    })
    
    print("히스토리:", cm.get_history())