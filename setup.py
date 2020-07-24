"""setup.py file for the package `darth_vader_rpi`.

The PyPi project name is Darth-Vader-RPi and the package name is
`darth_vader_rpi`.

"""

import os
from setuptools import find_packages, setup

from darth_vader_rpi import __version__


# Directory of this file
dirpath = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(dirpath, "README.rst")) as f:
    README = f.read()

setup(name='Darth-Vader-RPi',
      version=__version__,
      description='WRITEME',
      long_description=README,
      long_description_content_type='text/x-rst',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
      ],
      keywords='python raspberrypi rpi script',
      url='https://github.com/raul23/Darth-Vader-RPi',
      author='Raul C.',
      author_email='rchfe23@gmail.com',
      license='GPLv3',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'pygame',
          'py-common-utils @ https://github.com/raul23/py-common-utils/tarball/master'
      ],
      entry_points={
        'console_scripts': ['start_dv=darth_vader_rpi.start_dv:main']
      },
      zip_safe=False)
