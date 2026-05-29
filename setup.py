from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="fly-lang",
    version="1.0.0",
    author="Fly Language Project",
    description="Fly - A professional Python-powered scripting language with Kali Linux tool integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/fly-lang",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "fly=fly.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Security",
    ],
    keywords="fly language interpreter kali linux security scripting",
)
