from setuptools import setup, find_packages

setup(
    name="mozaik",
    version="0.1",
    packages=find_packages(exclude=["tests*", "experiment*"]),
    license="MIT",
    description="Create PowerPoint presentations programmatically",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=[],
    author="Aria Ghora Prabono",
    author_email="hello@ghora.net",
)
