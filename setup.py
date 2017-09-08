from distutils.core import setup, Extension
import glob

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
except ImportError:
    raise ImportError("Requires cython to "
            "be installed before running setup.py (pip install cython)")
try:
    import numpy as np
except ImportError:
    raise ImportError("Requires numpy to "
            "be installed before running setup.py (pip install numpy)")
try:
    import pysam
except ImportError:
    raise ImportError("Requires pysam to "
            "be installed before running setup.py (pip install pysam)")
try:
    import pyBigWig
except ImportError:
    raise ImportError("Requires pyBigWig to "
            "be installed before running setup.py (pip install pyBigWig)")
try:
    import cjson
except ImportError:
    raise ImportError("Requires python-cjson to "
            "be installed before running setup.py (pip install python-cjson)")
try:
    import scipy
except ImportError:
    raise ImportError("Requires scipy to "
            "be installed before running setup.py (pip install scipy)")

include_path = [np.get_include()]
include_path.extend(pysam.get_include())
ext_modules=cythonize([
        Extension('*', ['tgirt_seq_tools/*.pyx'],
            include_dirs = include_path)
])


setup(
    name='tgirt_seq_tools',
    version='0.1',
    description='Tools for TGIRT-seq pipeline',
    url='',
    author='Douglas Wu',
    author_email='wckdouglas@gmail.com',
    license='MIT',
    packages=['tgirt_seq_tools'],
    zip_safe=False,
    scripts = glob.glob('bin/*'),
    ext_modules = ext_modules,
    install_requires=[
          'cython',
          'numpy',
          'pysam>0.11.0',
          'matplotlib>=2.0.0',
          'seaborn>-0.7.1',
          'python-cjson>=1.2.0',
          'scipy>=0.19.0'
      ],
    cmdclass = {'build_ext': build_ext}
)
