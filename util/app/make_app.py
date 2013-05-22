#!/usr/bin/env python
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import shutil
import os
import stat
import subprocess
import glob

# Import the make_icon module, which uses ImageMagick and png2icns
# to make an application icon
if (not os.path.isfile('ko.icns') or
        os.path.getctime('ko.icns') < os.path.getctime('make_icon.py')):
    print "Generating icon using ImageMagick and png2icns"
    import make_icon

# Trick to make this run properly
import sys
sys.argv += ['py2app']

subprocess.call(['make'], cwd='../..')

try:    shutil.rmtree('build')
except OSError: pass

try:    shutil.rmtree('koko')
except OSError: pass

try:    os.remove('kokopelli.py')
except OSError: pass

try:    shutil.rmtree('kokopelli.app')
except OSError: pass

# This is the pythons script that we're bundling into an application.
shutil.copy('../../kokopelli','kokopelli.py')
shutil.copytree('../../koko','koko')

# Modify a line in __init__.py to store current hash
git_hash = subprocess.check_output(
    "git log --pretty=format:'%h' -n 1".split(' '))[1:-1]

if 'working directory clean' not in subprocess.check_output(['git','status']):
    git_hash += '+'

with open('koko/__init__.py', 'r') as f:
    lines = f.readlines()

with open('koko/__init__.py', 'w') as f:
    for L in lines:
        if 'HASH = None' in L:
            f.write("HASH = '%s'\n" % git_hash)
        else:
            f.write(L)


# Setup details for py2app
APP = ['kokopelli.py']
DATA_FILES = glob.glob('../../koko/lib/*.py')

OPTIONS = {'argv_emulation': True,
           'iconfile':'ko.icns'}

# Run py2app to bundle everything.
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

# Copy libtree
shutil.copy('../../libfab/libfab.dylib',
            'dist/kokopelli.app/Contents/Frameworks/libfab.dylib')
shutil.copytree('/Library/Frameworks/libpng.framework',
            'dist/kokopelli.app/Contents/Frameworks/libpng.framework')

# Copy the readme and examples into the distribution directory, then zip it up
shutil.rmtree('build')
shutil.rmtree('koko')
shutil.os.remove('kokopelli.py')

shutil.move('dist/kokopelli.app', '.')
shutil.rmtree('dist')

subprocess.call('zip -r kokopelli README kokopelli.app'.split(' '))

if 'mkeeter' in subprocess.check_output('whoami') and git_hash[-1] != '+':
    subprocess.call(
        'scp kokopelli.zip root@tmp.cba.mit.edu:/web/mkeeter'.split(' ')
    )