from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
#import distutils.extension

ext_network = Extension(
    name = 'openktn.lib.libnetwork',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libnetwork.f90'],
)

extensions_list=[]
extensions_lib=[ext_network]
extensions_list.extend(extensions_lib)

setup(
    name='openktn',
    version='0.0.1',
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    package_dir={'openktn': 'openktn'},
    packages=find_packages(),
    ext_modules=extensions_list,
    package_data={'openktn': []},
    scripts=[],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/OpenKTN',
    license='MIT',
    description="---",
    long_description="---",
)

