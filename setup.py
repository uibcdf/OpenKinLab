from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
#import distutils.extension

extensions_list=[]
extensions_lib=[]
extensions_list.extend(extensions_lib)

setup(
    name='openkinlab',
    version='0.0.1',
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    package_dir={'openkinlab': 'openkinlab'},
    packages=find_packages(),
    ext_modules=extensions_list,
    package_data={'openkinlab': []},
    scripts=[],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/OpenKinLab',
    license='MIT',
    description="---",
    long_description="---",
)

