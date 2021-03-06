from setuptools import setup

import os

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'
long_desc = open(root_dir + '/README.rst').read()

init = os.path.join(root_dir, 'djangosampler', '__init__.py')
version_line = [l for l in open(init) if l.startswith('VERSION')][0]
VERSION = eval(version_line.split('=')[-1])

setup(
    name='djangosampler',
    version=VERSION,
    description='Samples a percentage of SQL queries and groups them together for easy viewing',
    url='https://github.com/colinhowe/djangosampler',
    author='Colin Howe',
    author_email='colin@colinhowe.co.uk',
    packages=['djangosampler', 'djangosampler.plugins', 'djangosampler.migrations'],
    package_data={'djangosampler': ['templates/djangosampler/*', 'static/djangosampler/*']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='Apache 2.0',
    long_description=long_desc,
)
