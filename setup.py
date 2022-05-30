from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="DiscordUtils",
    author="Clutter Development",
    version="1.0.0",
    license="MIT",
    description="A collection of good and simple utilities for Discord bots.",
    install_requires=requirements,
    python_requires=">=3.10",
    py_modules=["discord_utils"],
    packages=["discord_utils"],
)
