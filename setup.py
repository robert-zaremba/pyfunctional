#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from setuptools import setup, Command  #, find_packages
from glob import glob
from unittest import TextTestRunner, TestLoader
import os
from os.path import splitext, basename, join as pjoin


try:
    import nose
except ImportError:
    nose = None
try:
    import pytest
except ImportError:
    pytest = None

class TestCommand(Command):
    """Custom distutils command to run the test suite."""

    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run_nose(self):
        """Run the test suite with nose."""
        return nose.core.TestProgram(argv=["", '-vv', pjoin(self._dir, 'tests')])

    def run_unittest(self):
        """Finds all the tests modules in zmq/tests/ and runs them."""
        testfiles = [ ]
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            name = splitext(basename(t))[0]
            if name.startswith('test_'):
                testfiles.append('.'.join(
                    ['tests', name])
                )
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 2)
        t.run(tests)

    def run_pytest(self):
        import subprocess
        errno = subprocess.call(['py.test','-q'])
        raise SystemExit(errno)

    def run(self):
        """Run the test suite, with py.test, nose, or unittest if nose is unavailable"""
        if pytest:
            self.run_pytest()
        elif nose:
            print ("pytest unavailable, trying test with nose. Some tests might not run, and some skipped, xfailed will appear as ERRORs.")
            self.run_nose()
        else:
            print ("pytest and nose unavailable, falling back on unittest. Skipped tests will appear as ERRORs.")
            return self.run_unittest()


setup(
    name='pyfunctional',
    version='0.0.1',
    use_2to3 = True,
    cmdclass = {'test': TestCommand},
    description="Enhance python functions and object to more functional style",
    long_description=codecs.open('README.md', "r", "utf-8").read(),
    author='Robert Zaremba',
    author_email='robert.marek.zaremba@wp.eu',
    url='https://github.com/robert-zaremba/tornado-pserver',
    download_url="https://github.com/robert-zaremba/tornado-pserver/tarball/master",
    license='Apache License',
    keywords="tornado server asynchronous protocol tcpserver netstring",
    packages=['functional'],
    install_requires=['tornado'],
    zip_safe=True,
    test_suite="nose.collector",
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        # "Development Status :: 3 - Alpha",
        # "Topic :: Utilities",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        # 'License :: OSI Approved :: Python Software Foundation License',
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: PyPy',
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking",
    ],
)
