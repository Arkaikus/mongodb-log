# -*- coding: utf-8 *-*
try:
    from setuptools import setup
except ImportError:
    from distutils import setup


long_description = open("README.rst").read()

setup(
    name='mongolog',
    version='0.1.3',
    description=':Maintainer: `Arkaikus`_',
    long_description=long_description,
    author='Andrei Savu',
    author_email='contact@andreisavu.ro',
    maintainer='Arkaikus',
    maintainer_email="arkaikus@outlook.com",
    url='https://github.com/Arkaikus/mongolog',
    packages=['mongolog'],
    keywords=["mongolog", "logging", "mongo", "mongodb"],
    install_requires=['pymongo'],
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System :: Logging",
        "Topic :: Database",
    ]
)
