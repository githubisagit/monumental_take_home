from setuptools import setup, find_packages

setup(
    name="brick-wall-simulator",
    version="1.0.0",
    description="Interactive brick wall construction simulator",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "brick-wall-simulator=brick_wall_simulator.main:main",
        ],
    },
)