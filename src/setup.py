from setuptools import setup, find_packages

setup(name='python-wink',
<<<<<<< HEAD
      version='0.7.8',
=======
      version='0.7.7',
>>>>>>> 1ecbdf56dde5d8b71ff6b2d131b7fd0c8fae50c7
      description='Access Wink devices via the Wink API',
      url='http://github.com/bradsk88/python-wink',
      author='Brad Johnson',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      zip_safe=True)
