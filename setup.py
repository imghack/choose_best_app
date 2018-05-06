from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='Analyze best apps by revenue',
      version='1.0',
      description=readme(),
      author='Maksym Romaniv',
      author_email='maksr51314@gmail.com',
      install_requires=required
      )
