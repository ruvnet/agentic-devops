import os
import re
from setuptools import setup, find_packages

# Helper function to read files
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Load requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Ensure that the aider package is included and version is imported correctly
aider_version = "0.1.0"
aider_init_path = os.path.join(os.path.dirname(__file__), 'devops', 'aider_chat', 'aider', '__init__.py')
if os.path.isfile(aider_init_path):
    with open(aider_init_path) as f:
        for line in f:
            match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", line)
            if match:
                aider_version = match.group(1)
                break

setup(
    name="agentic-devops",
    version="0.1.0",
    author="Reuven Cohen",
    author_email="your-email@example.com",
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
)

# Ensure that the aider_chat package is installed
os.system(f'pip install devops/aider_chat')
