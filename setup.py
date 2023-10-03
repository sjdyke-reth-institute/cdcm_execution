"""Control-oriented dynamic and computational modeling framework

Author:
    Ilias Bilionis
    R Murali Krishnan

Date:
    03.30.2023

"""

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f]

setup(
    name='cdcm',
    version='0.9.7',
    description='Control-oriented Dynamic Computational Modeling Platform (CDCM)',
    long_description=readme,
    author='Ilias Bilionis, R Murali Krishnan, Sreehari Manikkan',
    author_email='ibilion@purdue.edu, mrajase@purdue.edu, smanikka@purdue.edu',
    url='',
    license=_license,
    packages=find_packages(exclude=('docs','examples','tests', 'cdcm_rcbuilding')),
    python_requires=">=3.6",
    install_requires=requirements,
)

