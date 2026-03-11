from setuptools import setup, find_packages

setup(
    name="agent-router",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    description="Zero-dependency model routing for AI agents — route to the right model based on input complexity",
    author="0co",
    license="MIT",
)
