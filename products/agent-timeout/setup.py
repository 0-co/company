from setuptools import setup, find_packages

setup(
    name="agent-timeout",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    description="Zero-dependency timeout and deadline enforcement for AI agent API calls",
    author="0co",
    license="MIT",
)
