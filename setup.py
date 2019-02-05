from setuptools import setup, find_packages

setup(name='pystm',
      version='0.00',
      description='Minimal Python STM Library',
      author='Chris Turner',
      author_email='cat@199tech.net',
      license='BSD',
      keywords = ['stm', 'memory'],
      url = 'https://github.com/ixcat/pystm',
      packages = find_packages(),
      install_requires = ['numpy'])

