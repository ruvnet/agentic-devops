import re
from setuptools import find_packages, setup
from pathlib import Path

# Adjust the paths for the new location of setup.py
base_dir = Path(__file__).resolve().parent

# Read the requirements from the requirements.txt file
requirements_path = base_dir / "devops/requirements.txt"
if not requirements_path.exists():
    raise FileNotFoundError(f"Could not find requirements.txt at {requirements_path}")

with open(requirements_path) as f:
    requirements = f.read().splitlines()

# Ensure that __version__ is defined in the agentic_devops package
__version__ = "0.0.8"

# Read the long description from the README.md file
readme_path = base_dir / "README.md"
if not readme_path.exists():
    raise FileNotFoundError(f"Could not find README.md at {readme_path}")

with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()
    long_description = re.sub(r"\n!\[.*\]\(.*\)", "", long_description)  # Remove images
    long_description = re.sub(r"\n- \[.*\]\(.*\)", "", long_description)  # Remove links

# Setup configuration
setup(
    name="Agentic-DevOps",
    version="0.0.8",
    author="rUv",
    author_email="null@ruv.net",
    description="Agentic DevOps Tool for automating and managing various DevOps tasks and configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ruvnet/agentic-devops",
    packages=find_packages(where="devops"),
    package_dir={"": "devops"},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "agentic-devops=aider.main_wrapper:main",
            "agentic-devops-cli=aider.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
