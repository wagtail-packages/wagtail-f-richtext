#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from wagtail_f_richtext import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail-f-richtext",
    version=__version__,
    description="A replacement for the Wagtail richtext filter to use with a css framework.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Nick Moreton",
    author_email="nickmoreton@me.com",
    url="https://github.com/nickmoreton/wagtail-f-richtext",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
    ],
    install_requires=["Django>=3.0,<4.0", "Wagtail>=2.15,<2.16"],
    extras_require={
        "testing": ["dj-database-url==0.5.0", "freezegun==0.3.15"],
    },
    zip_safe=False,
)
