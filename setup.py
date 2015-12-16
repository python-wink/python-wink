from setuptools import setup

setup(name='python-wink',
      version='0.3.1',
      description='Access Wink devices via the Wink API',
      url='http://github.com/bradsk88/python-wink',
      author='John McLaughlin',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=['pywink'],
      zip_safe=True)
