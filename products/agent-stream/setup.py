from setuptools import setup, find_packages

setup(
    name="agent-stream",
    version="0.1.0",
    description="Streaming LLM response handling for AI agents. Collect chunks, track tokens, handle cancellation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="0co",
    url="https://github.com/0-co/company/tree/master/products/agent-stream",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
