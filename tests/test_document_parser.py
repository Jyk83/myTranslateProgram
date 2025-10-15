"""
문서 파싱 모듈 테스트
"""

import unittest
import os
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.document_parser import DocumentParser, DocumentContent


class TestDocumentParser(unittest.TestCase):
    """문서 파서 테스트 클래스"""
    
    def setUp(self):
        """테스트 초기화"""
        self.parser = DocumentParser()
        
    def test_supported_formats(self):
        """지원 형식 확인 테스트"""
        expected_formats = ['.xlsx', '.docx', '.pptx', '.pdf']
        self.assertEqual(self.parser.supported_formats, expected_formats)
        
    def test_document_content_creation(self):
        """DocumentContent 객체 생성 테스트"""
        content = DocumentContent()
        
        # 기본 속성 확인
        self.assertEqual(content.content_type, "")
        self.assertEqual(content.original_format, "")
        self.assertEqual(content.text_content, [])
        self.assertEqual(content.formatting_info, {})
        self.assertEqual(content.metadata, {})
        
    def test_add_text_block(self):
        """텍스트 블록 추가 테스트"""
        content = DocumentContent()
        
        # 텍스트 블록 추가
        content.add_text_block(
            "테스트 텍스트", 
            {"page": 1, "line": 1}, 
            {"font": "Arial", "size": 12}
        )
        
        # 추가된 블록 확인
        self.assertEqual(len(content.text_content), 1)
        block = content.text_content[0]
        
        self.assertEqual(block['text'], "테스트 텍스트")
        self.assertEqual(block['location']['page'], 1)
        self.assertEqual(block['formatting']['font'], "Arial")
        
    def test_file_not_found_error(self):
        """존재하지 않는 파일 처리 테스트"""
        non_existent_file = "non_existent_file.xlsx"
        
        # 파일이 존재하지 않을 때 None 반환 확인
        result = self.parser.parse_document(non_existent_file)
        self.assertIsNone(result)
        
    def test_unsupported_format_error(self):
        """지원되지 않는 형식 처리 테스트"""
        # 임시 파일 생성
        test_file = "test_file.txt"
        with open(test_file, 'w') as f:
            f.write("Test content")
            
        try:
            # 지원되지 않는 형식일 때 None 반환 확인
            result = self.parser.parse_document(test_file)
            self.assertIsNone(result)
        finally:
            # 임시 파일 정리
            if os.path.exists(test_file):
                os.remove(test_file)


class TestDocumentContentIntegration(unittest.TestCase):
    """문서 내용 통합 테스트"""
    
    def test_multiple_text_blocks(self):
        """다중 텍스트 블록 처리 테스트"""
        content = DocumentContent()
        content.content_type = "test"
        content.original_format = ".txt"
        
        # 여러 텍스트 블록 추가
        test_blocks = [
            ("첫 번째 블록", {"section": 1}, {"bold": True}),
            ("두 번째 블록", {"section": 2}, {"italic": True}),
            ("세 번째 블록", {"section": 3}, {"underline": True})
        ]
        
        for text, location, formatting in test_blocks:
            content.add_text_block(text, location, formatting)
            
        # 블록 수 확인
        self.assertEqual(len(content.text_content), 3)
        
        # 각 블록 내용 확인
        for i, (expected_text, expected_location, expected_formatting) in enumerate(test_blocks):
            block = content.text_content[i]
            self.assertEqual(block['text'], expected_text)
            self.assertEqual(block['location'], expected_location)
            self.assertEqual(block['formatting'], expected_formatting)


if __name__ == '__main__':
    # 테스트 실행
    unittest.main(verbosity=2)