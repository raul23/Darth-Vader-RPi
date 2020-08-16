.. _config file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _default values: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _"I am your father": https://www.youtube.com/watch?v=xuJEYdOFEP4
.. _Imperial March song by Jacob Townsend: https://soundcloud.com/jacobtownsend1/imperial-march
.. _"Nooooo": https://www.youtube.com/watch?v=ZscVhFvD6iE
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

`:warning:`

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
   </div>

* The lightsaber is illuminated by 3 LEDs connected in parallel
* The *Bottom*, *Middle*, and *Top* LEDs illuminate the slots in Darth Vader's
  chest control box. They blink in a specific sequence as specified in the
  `config file`_. See ``TODO`` to know how to change this sequence.
* When the *Lightsaber button* is first pressed, it produces the sound of
  drawing the sword, illuminates it, and a hum sound persists until the
  lightsaber is turned off. If the button is pressed again, it produces the
  sound of retracting the lightsaber and turns it off.

  **NOTE:** the *Lightsaber button* can be pressed while the *Song button* or
  the *Quotes button* is playing audio since they use different channels.
* The *Song button* plays the `Imperial March song by Jacob Townsend`_
* The *Quotes button* plays a famous Darth Vader's quotes when pressed. For
  testing purposes, the ``darth_vader_rpi`` package comes with two movie lines:

  * `"I am your father"`_
  * `"Nooooo"`_

  However, you could add more if you want to. Check ``TODO`` for more info on
  how to do it.

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
Script ``start_dv``
-------------------
Once you install ``darth_vader_rpi``, you should have access to the script
``start_dv`` which turns on LEDs and plays sound effects on a Raspberry Pi.

Run the script on your RPi with `default values`_ for the GPIO channels and other
settings::

   $ start_dv

If you want to test the script on your computer (use the `-s` option)::

   $ start_dv -s

`:information_source:`

   Both previous commands will use the default values from the `config file`_
   (e.g GPIO and audio channels).

   To change these settings, use the `-e` flag to edit the configuration file
   with your favorite editor and don't forget to save your changes::

      $ start_dv -e

List of options
^^^^^^^^^^^^^^^
Test

Simulating on your computer
---------------------------
If you don't have access to a Raspberry Pi and want to try out the script
``start_dv``, you can use the `-s` flag which will simulate an RPi on your
computer. It will make use of the library ``SimulRPi`` to simulate LEDs and
push buttons by blinking red circles on the terminal and monitoring pressed
keyboard keys::

   $ start_dv -s

**NOTE:** the last command makes use of default values. See ``TODO`` on how
to change these settings.

Here is a video of what it looks like on a terminal when running the script
``start_dv`` on a computer instead of an RPi:

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/watch?v=Wfv5uaQtRM4"><img src="https://img.youtube.com/vi/Wfv5uaQtRM4/0.jpg" alt="Raspberry Pi simulaion on a terminal"></a>
   <p><b>Click on the above image for the full video</b></p>
   </div>



Change default settings
-----------------------

Add Darth Vader quotes
^^^^^^^^^^^^^^^^^^^^^^

Change channel volume
^^^^^^^^^^^^^^^^^^^^^

Change key to channel mapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change paths to audio files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change GPIO channels
^^^^^^^^^^^^^^^^^^^^

Change slot LEDs sequence
^^^^^^^^^^^^^^^^^^^^^^^^^

Mute breathing and closing sounds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change Log
==========
0.1.0a0
-------
* Test

TODOs
=====
* Test
* Bouncy button

Resources
=========
* Darth-Vader-RPi GitHub: source code
* Darth-Vader-RPi PyPI

References
==========
* pygame: package used for
* RPI.GPIO:
* SimulRPi:

Credits
=======
* Darth Vader quotes:

  * `"I am your father"`_
  * `"Nooooo"`_
* `Imperial March song by Jacob Townsend <https://soundcloud.com/jacobtownsend1/imperial-march>`_
  is licensed under a `Creative Commons (CC BY-NC-SA 3.0) License <http://creativecommons.org/licenses/by-nc-sa/3.0/>`_
  
  * Old code used `Star Wars- The Imperial March (Darth Vader's Theme) <https://www.youtube.com/watch?v=-bzWSJG93P8>`_
* Sound effects:

  * `Darth Vader breathing sound <https://www.youtube.com/watch?v=d28NrjMPERs>`_
  * `Darth Vader's lightsaber sound effect <https://www.youtube.com/watch?v=bord-573NWY>`_
  * `Darth Vader's lightsaber retraction sound effect <https://www.youtube.com/watch?v=m6buyGJF46k>`_
