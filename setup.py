""" pypi setup for track-ml """
from setuptools import setup, find_packages

install_requires = [
    "pandas>=0.20.1",
    'absl-py>=0.1.13',
    'pyyaml>=3.12'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="track-ml",
    author="RISE",
    version="0.1.1",
    description="Experiment tracking module",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richardliaw/track",
    license='MIT License',
    packages=find_packages(),
)
