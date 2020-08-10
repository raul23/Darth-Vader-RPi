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

# The text of the requirements.txt file
with open(os.path.join(dirpath, "requirements.txt")) as f:
    REQUIREMENTS = f.read().split()

setup(name='Darth-Vader-RPi',
      version=__version__,
      description='WRITEME',
      long_description=README,
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        # 'Topic :: Software Development :: Libraries :: pygame',
      ],
      keywords='Raspberry Pi script pygame starwars Darth Vader',
      url='https://github.com/raul23/Darth-Vader-RPi',
      author='Raul C.',
      author_email='rchfe23@gmail.com',
      license='GPLv3',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      install_requires=REQUIREMENTS,
      entry_points={
        'console_scripts': ['start_dv=darth_vader_rpi.start_dv:main']
      },
      zip_safe=False)
