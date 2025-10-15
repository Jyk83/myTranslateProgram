"""
Document Translator 설정 파일
pip 패키지로 설치할 때 사용
"""

from setuptools import setup, find_packages
import os

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements.txt에서 의존성 읽기
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="document-translator",
    version="1.0.0",
    author="Document Translator Team",
    author_email="support@documenttranslator.com",
    description="Windows용 다국어 문서 번역 프로그램",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/document-translator",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/document-translator/issues",
        "Documentation": "https://github.com/your-username/document-translator/wiki",
        "Source Code": "https://github.com/your-username/document-translator",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
        ],
        "build": [
            "pyinstaller>=5.0",
        ],
    },
    package_data={
        "document_translator": [
            "config.ini",
            "assets/*",
            "docs/*",
        ],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "document-translator=main:main",
        ],
        "gui_scripts": [
            "document-translator-gui=main:main",
        ],
    },
    keywords=[
        "translation", "document", "translator", "excel", "word", 
        "powerpoint", "pdf", "openai", "gpt", "google-translate",
        "multilingual", "windows", "desktop", "gui", "pyqt5"
    ],
    zip_safe=False,
)