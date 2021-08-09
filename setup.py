from setuptools import setup, find_packages

setup(
    name='alfred',
    version='0.1.0',
    packages=find_packages(include=['alfred', 'alfred.*'])
)

