import os
import re
import sys
import subprocess
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

# Helper function to read files
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Custom command to install aider_chat
class CustomDevelopCommand(develop):
    def run(self):
        # Ensure pip is installed
        subprocess.check_call([sys.executable, '-m', 'ensurepip'])
        # Navigate to the aider_chat directory and run pip install .
        os.chdir('devops/aider_chat')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '.'])
        os.chdir('../../')  # Change back to the root directory
        develop.run(self)

class CustomInstallCommand(install):
    def run(self):
        # Ensure pip is installed
        subprocess.check_call([sys.executable, '-m', 'ensurepip'])
        # Navigate to the aider_chat directory and run pip install .
        os.chdir('devops/aider_chat')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '.'])
        os.chdir('../../')  # Change back to the root directory
        install.run(self)

# Load requirements from the main requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Load requirements from the aider_chat requirements.txt file
aider_chat_requirements_path = os.path.join('devops', 'aider_chat', 'requirements.txt')
if os.path.isfile(aider_chat_requirements_path):
    with open(aider_chat_requirements_path) as f:
        requirements += f.read().splitlines()

# Ensure that the aider package is included and version is imported correctly
aider_version = "0.1.0"
aider_init_path = os.path.join('devops', 'aider_chat', 'aider', '__init__.py')
if os.path.isfile(aider_init_path):
    with open(aider_init_path) as f:
        for line in f:
            match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", line)
            if match:
                aider_version = match.group(1)
                break

setup(
    name="agentic-devops",
    version="0.0.4",
    author="rUv",
    author_email="null@ruv.net",
    description="Agentic DevOps Tool for automating and managing various DevOps tasks and configurations.",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url="https://github.com/ruvnet/agentic-devops",
    packages=find_packages(where="devops"),
    package_dir={"": "devops"},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "agentic-devops=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'develop': CustomDevelopCommand,
        'install': CustomInstallCommand,
    },
)
