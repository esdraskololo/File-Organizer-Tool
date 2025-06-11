from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-organizer-tool",
    version="1.0.0",
    description="A tool to organize files into subdirectories based on filename prefixes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MC Oruç",
    author_email="kaanyildiz@trakya.edu.tr",
    url="https://github.com/MC-Oruc/file-organizer-tool.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Turkish",
        "Natural Language :: German",
        "Natural Language :: Spanish",
        "Natural Language :: French",
        "Natural Language :: Italian",
        "Natural Language :: Portuguese",
        "Natural Language :: Japanese",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Russian",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "file-organizer=main:main",
            "fileorg=main:main",
        ],
    },
)
