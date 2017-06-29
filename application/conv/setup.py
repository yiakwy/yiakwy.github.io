#!/usr/bin/env python2.7

from distutils.core import setup
from distutils.extension import Extension

import sys
import os

from distutils import sysconfig
Makefile = sysconfig.get_makefile_filename()
print("makefile is" + " " + Makefile)


if sys.platform == 'darwin':
    vars = sysconfig.get_config_vars()
    print("LDSHARED-bf: " + vars.get('LDSHARED',"nothing"))
    print("with type" + " " +  str(type(vars['LDSHARED'])))
    # vars['LDSHARED'] = vars['LDSHARED'].replace('-bundle', '-dynamiclib')
    vars['LDSHARED'] = vars['LDSHARED'].replace('-arch i386',  '')
    vars = sysconfig.get_config_vars()
    print("LDSHARED-af: " + vars.get('LDSHARED',"nothing"))

fft_module = Extension('fft',
        include_dirs = ["./include",
                        "/usr/local/Cellar/boost157/1.57.0/include/",
                        "/usr/include/python2.7",
                        "/usr/local/include"],
        libraries = ["boost_python", "dl", "python2.7"],
        library_dirs = ["/System/Library/Frameworks/Python.framework/Versions/2.7/lib",
                        "/usr/local/Cellar/boost-python157/1.57.0/lib/",
                        # "/usr/local/Cellar/boost157/1.57.0/lib/",
                        "/usr/local/lib",
                        ],
        sources = ['./src/fft_module.cpp'],
        extra_compile_args=['-std=c++11', '-stdlib=libstdc++', '-shared']) 
#https://stackoverflow.com/questions/35006614/what-does-symbol-not-found-expected-in-flat-namespace-actually-mean

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

meta = dict(
	name = 'fft',
	description="fast fft for deep conv operation",
	long_description = __doc__,
	download_url = "https://github.com/yiakwy/yiakwy.github.io",
	license = 'MIT',
	classifiers = [f for f in CLASSIFIERS.split('\n') if f],
	author = 'iphtmOfwr',
	author_email = 'lwang11@mtu.edu',
	url = 'yiakwy.github.io',
	ext_modules = [fft_module]				
)

if __name__ == "__main__":
	setup(**meta)
