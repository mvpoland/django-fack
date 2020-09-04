import os
from setuptools import setup, find_packages

import fack


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-fack',
    version=fack.__version__,
    description='A simple FAQ application for Django sites.',
    long_description=read('README.rst'),
    license="BSD",

    author='Kevin Fricovsky',
    author_email='kfricovsky@gmail.com',
    url='http://django-fack.rtfd.org/',

    packages=find_packages(exclude=['example']),
    zip_safe=False,

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
    ],

    install_requires=[
        'Django>=1.11,<3.0',
        'future',
        'Pillow',
    ],
)
