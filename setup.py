from setuptools import setup

setup(name='holst',
  version='0.1',
  description='Generate iptables files from yaml dsl',
  author='Alex Wilson',
  author_email='a.wilson@alumni.warwick.ac.uk',
  packages=['holst', 'holst.parser', 'holst.core'],
  package_data = {
        'holst': ['templates/rules.tpl'],
  },
  entry_points = {
  'console_scripts': ['holst=holst:main']
  },
  include_package_data=True,
  zip_safe=False)
