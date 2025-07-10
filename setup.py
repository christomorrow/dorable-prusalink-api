# setup.py
from setuptools import setup, find_packages

setup(
    name='dorable_prusalink_api',
    version='0.1.0',
    packages=find_packages(),
    description='Python library for Prusa Link',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/christomorrow/dorable-prusalink-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)