from setuptools import setup, find_packages

# Read long description from file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read requirements from file
install_requires = []
with open("requirements.txt") as fh:
    install_requires = fh.read().splitlines()

setup(
    name="{{cookiecutter.project_slug}}",
    version="{{cookiecutter.project_version}}",
    description="{{cookiecutter.project_description}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="{{cookiecutter.project_git_repo}}",
    author="{{cookiecutter.author_name}}",
    author_email="{{cookiecutter.author_email}}",
    maintainer="{{cookiecutter.author_name}}",
    maintainer_email="{{cookiecutter.author_email}}",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            '{{cookiecutter.project_slug}} = src.{{cookiecutter.project_slug}}:main',
        ],
    },
    keywords=(
        '{{cookiecutter.project_tags}}'
    ),
    project_urls={
        "Repository": "{{cookiecutter.project_git_repo}}",
        "Tracker": "{{cookiecutter.project_git_repo}}/issues",
    },
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    setup_requires=[
        "setuptools_git == 1.2",
    ],
)
