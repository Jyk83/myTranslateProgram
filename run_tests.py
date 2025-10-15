#!/usr/bin/env python3
"""
Document Translator 테스트 실행 스크립트
"""

import unittest
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_tests():
    """테스트 실행"""
    # 테스트 디스커버리
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 결과 반환
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("Document Translator 테스트 실행")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("\n❌ 일부 테스트 실패!")
        sys.exit(1)