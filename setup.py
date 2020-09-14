"""setup.py file for the package ``darth_vader_rpi``.

The PyPi project name is ``Darth-Vader-RPi`` and the package name is
``darth_vader_rpi``.

"""

import os
import sys
from setuptools import find_packages, setup

from darth_vader_rpi import __version__, __test_version__


# Choose the correct version based on script's arg
if len(sys.argv) > 1 and sys.argv[1] == "testing":
    VERSION = __test_version__
    # Remove "testing" from args so setup doesn't process "testing" as a cmd
    sys.argv.remove("testing")
else:
    VERSION = __version__

# Directory of this file
dirpath = os.path.abspath(os.path.dirname(__file__))

# The text of the README file (used on PyPI)
with open(os.path.join(dirpath, "README.rst"), encoding="utf-8") as f:
    README = f.read()

# The text of the requirements.txt file
with open(os.path.join(dirpath, "requirements.txt")) as f:
    REQUIREMENTS = f.read().splitlines()


setup(name='Darth-Vader-RPi',
      version=VERSION,
      description='A Raspberry Pi project about activating a Darth Vader '
                  'action figure by turning on LEDs on his suit and '
                  'lightsaber, and by playing sounds such as some of his '
                  'famous quotes.',
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
      project_urls={  # Optional
          'Bug Reports': 'https://github.com/raul23/Darth-Vader-RPi/issues',
          'Documentation': 'https://darth-vader-rpi.readthedocs.io/',
          'Source': 'https://github.com/raul23/Darth-Vader-RPi',
      },
      zip_safe=False)
