from setuptools import setup

install_requires = [
    "pandas>=0.20.1",
    'absl-py>=0.1.13',
]

setup(
    name="track",
    author="RISE",
    install_requires=install_requires,
    packages=["track"],
    package_dir={"track": "track"}
)
