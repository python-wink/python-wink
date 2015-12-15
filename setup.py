from setuptools import setup

setup(name='python-wink',
      version='0.3',
      description='Access Wink devices via the Wink API',
      url='http://github.com/balloob/python-wink',
      author='John McLaughlin',
      license='MIT',
      install_requires=['requests>=2.0', 'mock'],
      packages=['pywink'],
      zip_safe=True)
