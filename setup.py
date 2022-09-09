from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f]

setup(
    name='cdcm',
    version='0.0.1',
    description='Control-oriented Dynamic Computational Modeling Platform (CDCM)',
    long_description=readme,
    author='',
    author_email='',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires=">=3.6",
    install_requires=requirements,
)

