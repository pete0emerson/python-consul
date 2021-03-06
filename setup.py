import glob
import sys
import re
import os

from setuptools.command.test import test as TestCommand
from setuptools import setup


metadata = dict(
    re.findall("__([a-z]+)__ = '([^']+)'", open('consul/__init__.py').read()))


requirements = [
    x.strip() for x
    in open('requirements.txt').readlines() if not x.startswith('#')]


description = "Python client for Consul (http://www.consul.io/)"


py_modules = [os.path.splitext(x)[0] for x in glob.glob('consul/*.py')]

try:
    import asyncio
    del asyncio
except:
    if 'consul/aio' in py_modules:
        py_modules.remove('consul/aio')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='python-consul',
    version=metadata['version'],
    author='Andy Gayton',
    author_email='andy@thecablelounge.com',
    url='https://github.com/cablehead/python-consul',
    license='MIT',
    description=description,
    long_description=open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read(),
    py_modules=py_modules,
    install_requires=requirements,
    extras_require={
        'tornado': ['tornado'],
        'asyncio': ['aiohttp'],
    },
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
