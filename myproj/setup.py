from setuptools import setup, find_packages

# Read requirements from file
install_requires = []
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="myproj",
    version='0.1.0',
    packages=find_packages(),
    #packages=['myproj'],
    install_requires=install_requires,
)

