from distutils.core import setup	
from Cython.Build import cythonize	

setup(
    ext_modules = cythonize("simann_optimize_cy3.pyx")
)




