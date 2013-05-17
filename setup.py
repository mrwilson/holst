from setuptools import setup

setup(name='holst',
  version='0.1',
  description='Generate iptables files from yaml dsl',
  author='Alex Wilson',
  author_email='a.wilson@alumni.warwick.ac.uk',
  packages=['holst', 'holst.parser', 'holst.core'],
  entry_points = {
  'console_scripts': ['holst=holst:main']
  },
  zip_safe=False)
