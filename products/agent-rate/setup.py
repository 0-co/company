from setuptools import setup, find_packages

setup(
    name="agent-rate",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    description="Zero-dependency rate limiting for AI agent API calls",
    author="0co",
    license="MIT",
)
