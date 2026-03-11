from setuptools import setup, find_packages

setup(
    name="agent-fallback",
    version="0.1.0",
    description="Zero-dependency multi-provider failover for AI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="0co",
    url="https://github.com/0-co/company/tree/master/products/agent-fallback",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    keywords="llm agent fallback failover anthropic openai reliability",
)
