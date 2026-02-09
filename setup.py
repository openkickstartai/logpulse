from setuptools import setup, find_packages

setup(
    name="logpulse",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click>=8.0"],
    entry_points={
        "console_scripts": [
            "logpulse=logpulse.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="nexus-7 (via OpenKickstart)",
    description="Lightweight CLI log analyzer",
)
