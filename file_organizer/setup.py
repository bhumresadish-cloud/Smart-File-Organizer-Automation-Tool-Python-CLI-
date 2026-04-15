"""Setup configuration for pip installation."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-file-organizer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional file management automation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-organizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer[all]==0.9.0",
        "watchdog==3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "file-organizer=main:app",
        ],
    },
    include_package_data=True,
)
