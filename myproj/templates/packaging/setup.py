from setuptools import setup, find_packages

{{cookiecutter.replace.packaging.long_description}}

{{cookiecutter.replace.packaging.requirements}}

setup(
    name="{{cookiecutter.project.slug}}",
    version="{{cookiecutter.project.version}}",
    description="{{cookiecutter.project.synopsis}}",
{{cookiecutter.replace.packaging.long_description_argument}}
    url="{{cookiecutter.project.git_repo}}",
    author="{{cookiecutter.project.original_author}}",
    maintainer="{{cookiecutter.user.name}}",
    maintainer_email="{{cookiecutter.user.email}}",
{{cookiecutter.replace.packaging.entry_points_argument}}
    keywords=(
        '{{cookiecutter.project.tags}}'
    ),
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    setup_requires=[
        "setuptools_git",
    ],
)
