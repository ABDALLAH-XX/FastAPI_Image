# setup.py
from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'mon_traitement',
        ['src/main.cpp'],
        include_dirs=[pybind11.get_include(), '/usr/include/opencv4'],
        libraries=['opencv_core', 'opencv_imgproc'],
        language='c++'
    ),
]

setup(name='mon_traitement', ext_modules=ext_modules)