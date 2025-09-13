#!/usr/bin/env python3 

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    author_email = "c.ogcae@engineer.com",
    name         = "cryptoforge",
    version      = "1.0.2",
    author       = "ogcae",

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ogcae/cryptoforge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    keywords="rsa encryption cryptography security pkcs1 digital-signatures",
    project_urls={
        "Bug Reports": "https://github.com/ogcae/cryptoforge/issues",
        "Source": "https://github.com/ogcae/cryptoforge",
        "Documentation": "https://github.com/ogcae/cryptoforge/blob/main/README.md",
    },
    extras_require={
        "web": ["flask>=2.0.0"],
        "dev": ["pytest>=6.0.0", "black", "flake8"],
    },
)
