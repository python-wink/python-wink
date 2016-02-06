from setuptools import setup

setup(name='python-wink',
      version='0.5.0',
      description='Access Wink devices via the Wink API',
      url='http://github.com/bradsk88/python-wink',
      author='Brad Johnson',
      license='MIT',
      install_requires=['requests>=2.0', 'ijson==2.3'],
      tests_require=['mock'],
      test_suite='tests',
      packages=['pywink'],
      zip_safe=True)
