#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from setuptools.command.install import install

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from ngosubs/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("ngosubs", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

install_requires = [
    'future',
    'django-ngoshop', 
]

post_install_requires = [i for i in install_requires if ('-' in i or ':' in i or '.' in i)]
install_requires = [i for i in install_requires if not ('-' in i or ':' in i or '.' in i)]


# for setuptools to work properly, we need to install packages with - or : separately
# and for that we need a hook
# https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if post_install_requires:
            cmd = ['pip', 'install', '-q'] + post_install_requires
            subprocess.check_call(cmd)
        install.run(self)

setup(
    name='django-ngosubs',
    version=version,
    description="""django plugin to add subscription to django-cms/shop""",
    long_description=readme + '\n\n' + history,
    author='Cedric ROMAN',
    author_email='roman@numengo.com',
    url='https://github.com/numengo/django-ngosubs',
    packages=[
        'ngosubs',
    ],
    include_package_data=True,
    install_requires=install_requires,
    requires=install_requires,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass = {
        'install': PostInstallCommand,
        # 'develop': PostInstallCommand,
    },
)
