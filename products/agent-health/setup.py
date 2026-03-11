from setuptools import setup, find_packages

setup(
    name="agent-health",
    version="0.1.0",
    description="Health checks for AI APIs. Know before your agents do.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="0co",
    url="https://github.com/0-co/company/tree/master/products/agent-health",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
