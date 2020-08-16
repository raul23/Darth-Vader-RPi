.. _config file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _default values: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _RPi.GPIO: https://pypi.org/project/RPi.GPIO/
.. _SimulRPi: https://github.com/raul23/SimulRPi

======
README
======
.. raw:: html

   <p align="center"><img src="https://raw.githubusercontent.com/raul23/Darth-Vader-RPi/master/docs/_static/images/Darth_Vader_RPi_logo.png">
   <br>🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
   </p>

.. image:: https://readthedocs.org/projects/darth-vader-rpi/badge/?version=latest
   :target: https://darth-vader-rpi.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/raul23/Darth-Vader-RPi.svg?branch=master
   :target: https://travis-ci.org/raul23/Darth-Vader-RPi
   :alt: Build Status

**Darth-Vader-RPi** is a Python-based Raspberry Pi (RPi) project about activating a Darth
Vader action figure by turning on LEDs on his suit and lightsaber, and by 
playing sounds such as some of his famous quotes.

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/embed/P631S1k1h_0">
   <img src="https://raw.githubusercontent.com/raul23/images/master/Darth-Vader-RPi/darth_vader_lightsaber_2x_speed_smaller_version.gif"/>
   </a>
   <p><b>Turning on/off the lightsaber</b></p>
   </div>

.. important::

   If you don't have an RPi, don't worry. You can still test the program on
   your own computer because the package ``darth_vader_rpi`` uses the library
   `SimulRPi`_ to simulate I/O devices connected to an RPi such as LEDs and
   push buttons by blinking small circles on the terminal and playing sounds
   when a keyboard key is pressed. Almost like testing with a real RPi!

   **Disclaimer:** I also wrote the `SimulRPi`_ library

.. contents::
   :depth: 3
   :local:

Introduction
============

The Darth Vader action figure is 11.5 inches tall (which is `this one from
Hasbro <https://amzn.to/3hIw0ou>`_) and was modified to make it more lifelike
by illuminating the lightsaber, chest control box, and belt. 3 push buttons 
control the following sounds:

#. Some of his famous quotes
#. The Imperial march theme song
#. The lightsaber opening and closing sounds and its illumination

His iconic breathing sound plays in the background indefinitely as soon as the
RPi is run with the script.

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/embed/P631S1k1h_0"><img src="https://img.youtube.com/vi/P631S1k1h_0/0.jpg" alt="Darth Vader action figure activated"></a>
   <p><b>Click on the above image for the full video so you can also hear the
   different sounds produced by pressing the push buttons</b></p>
   </div>

Connection diagram
==================
.. raw:: html

   <div align="center">
   <img src="https://raw.githubusercontent.com/raul23/images/master/Darth-Vader-RPi/schematics.png"/>
   <p><b>Schematics</b></p>
   </div>

Dependencies
============
* **Platforms:** macOS, Linux
* **Python**: 3.5, 3.6, 3.7, 3.8
* **Packages**

  * ``pygame``>=1.9.6: for playing sounds
  * ``SimulRPi`` >=0.0.1a0: for partly faking `RPI.GPIO`_ and simulating I/O
    devices connected to an RPi such as LEDs and push buttons in case that you
    don't have access to an RPi. See `SimulRPi`_ for more info about this
    library.

Installation instructions
=========================
1. Install the ``darth_vader_rpi`` package with *pip*::

   $ pip install Darth-Vader-RPi

   It will install the dependencies if they are not already found in your system.

2. Test your installation by importing ``darth_vader_rpi`` and printing its version::

   $ python -c "import darth_vader_rpi; print(darth_vader_rpi.__version__)"

Usage
=====
Script ``darth_vader_rpi``
--------------------------
Once you install ``darth_vader_rpi``, you should have access to the script
``start_dv`` which turns on LEDs and plays sound effects on a Raspberry Pi.

Run the script on your RPi with `default values`_ for the GPIO channels and other
settings::

   $ start_dv

If you want to test the script on your computer (use the `-s` option)::

   $ start_dv -s

.. note::

   Both previous commands will use the default values from the `config file`_
   (e.g GPIO and audio channels).

   To change these settings, use the `-e` flag to edit the configuration file
   with your favorite editor and don't forget to save your changes::

      $ start_dv -e

List of options
---------------
Test