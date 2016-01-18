from os.path import join, dirname
from setuptools import setup, find_packages



excludes = (
    '*test*',
    '*local_settings*',
) # yapf: disable

setup(name='py-mancala',
      version='1.0',
      license='MIT',
      description='Mancala solver for Python',
      author='Krzysztof Dorosz',
      author_email='cypreess@gmail.com',
      url='https://github.com/cypreess/py-mancala',
      platforms=['Any'],
      packages=find_packages(exclude=excludes),
      install_requires=[],
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5'])
