#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="django-anonymizer",
    version='0.5.0.15-bw',
    packages=find_packages(exclude=['*.tests']),
    include_package_data=True,

    author="Luke Plant",
    author_email="L.Plant.98@cantab.net",
    maintainer="David Stensland",
    maintainer_email="anonymizer@terite.com",
    url="https://github.com/betterworks/django-anonymizer",
    description="App to anonymize data in Django models.",
    long_description=(read('README.rst') + "\n\n" + read('CHANGES.rst')),
    license="MIT",
    keywords="django data database anonymize private",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
        "Topic :: Software Development :: Testing",
        "Topic :: Database"
        ],
    install_requires=[
        'Faker >= 0.7.7',
        'django >= 1.8.0',
        'six >= 1.10.0'],
)
