from setuptools import setup, find_packages

setup(
    name="agent-trace",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    description="Distributed tracing for multi-agent workflows. Zero dependencies.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="0co",
    url="https://github.com/0-co/company",
    classifiers=["License :: OSI Approved :: MIT License"],
)
