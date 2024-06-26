======
README
======
.. raw:: html

   <p align="center"><img src="https://raw.githubusercontent.com/raul23/Darth-Vader-RPi/master/docs/_static/images/Darth_Vader_RPi_logo.png">
   </p>

.. image:: https://readthedocs.org/projects/darth-vader-rpi/badge/?version=latest
   :target: https://darth-vader-rpi.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/raul23/Darth-Vader-RPi.svg?branch=master
   :target: https://travis-ci.org/raul23/Darth-Vader-RPi
   :alt: Build Status

**Darth-Vader-RPi** is a Python-based Raspberry Pi (RPi) project about
activating a Darth Vader action figure by turning on LEDs on his suit and
lightsaber, and by playing sounds such as some of his famous quotes.

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/embed/P631S1k1h_0">
   <img src="https://raw.githubusercontent.com/raul23/images/master/Darth-Vader-RPi/darth_vader_lightsaber_2x_speed_smaller_version.gif"/>
   </a>
   <p><b>Turning on/off the lightsaber</b></p>
   </div>

`:star:`

   If you don't have an RPi, don't worry. You can still
   test the script on your own computer because the
   ``darth_vader_rpi`` package uses the `SimulRPi`_ library to simulate I/O
   devices connected to an RPi such as LEDs and push buttons by blinking red
   dots in the terminal and playing sounds when a keyboard key is pressed.
   Almost like testing with a real RPi!

   **Disclaimer:** I also wrote the `SimulRPi`_ library

Introduction
============
The Darth Vader action figure is 11.5 inches tall (which is
`this one from Hasbro`_) and was modified to make it more lifelike by
illuminating the lightsaber, chest control box, and belt. 3 push buttons
are connected to an RPi and control the following sounds and LEDs:

#. Some of his famous quotes
#. The *Imperial march* theme song
#. The lightsaber drawing, hum and retraction sounds
#. The lightbsaber illumination (3 LEDs)

His iconic breathing sound plays in the background almost as soon
as the RPi is run with the ``start_dv`` script.

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/embed/P631S1k1h_0"><img src="https://img.youtube.com/vi/P631S1k1h_0/0.jpg" alt="Darth Vader action figure activated"></a>
   <p><b>Click on the above image for the full video to see the LEDs turning on
   and hear the different sounds produced by pressing the push buttons</b></p>
   </div>

Connection diagram
==================
Here's how the various LEDs and push buttons are connected to the Raspberry Pi:

.. raw:: html

   <div align="center">
   <img src="https://raw.githubusercontent.com/raul23/images/master/Darth-Vader-RPi/schematics.png"/>
   </div>

* The lightsaber is illuminated by 3 LEDs connected in parallel.
* The *Top*, *Middle*, and *Bottom* LEDs illuminate the slots in Darth Vader's
  chest control box. They blink in a specific sequence
  `as specified in the configuration file`_.
* When the *Lightsaber button* is first pressed, it produces the drawing sound,
  illuminates the sword, and a hum sound persists until the *Lightsaber button*
  is turned off. If the button is pressed again, it produces the sound of
  retracting the lightsaber and turns it off.

  **NOTE:** the *Lightsaber button* can be pressed while the *Song button* or
  the *Quotes button* is playing audio since they use different audio channels.
* The *Song button* plays the `Imperial March song by Jacob Townsend`_.
* The *Quotes button* plays famous Darth Vader quotes when pressed. For
  testing purposes, the ``darth_vader_rpi`` package comes with two movie lines:

  * `"I am your father" (YouTube)`_
  * `"Nooooo" (YouTube)`_: it is also used for the `closing sound`_ when the
    ``start_dv`` script exits

  However, you could `add more quotes`_ if you want.

Dependencies
============
* **Platforms:** Linux, macOS
* **Python**: 3.5, 3.6, 3.7, 3.8
* **Packages**

  * ``dv_sounds``>=0.1.0a0: for retrieving the sound files (quotes, songs, and
    sound effects)

    - **Ref:** `dv_sounds`_
  * ``pygame``>=1.9.3: for playing sounds

    - **Ref:** `pygame`_
  * ``pynput``>=1.6.8: needed by ``SimulRPi`` for monitoring the keyboard when
    simulating push buttons with keyboard keys, i.e. when running the
    ``start_dv`` script in simulation mode

    - **Ref:** `pynput`_
  * ``SimulRPi`` >=0.1.0a0: for partly faking `RPI.GPIO`_ and simulating I/O
    devices connected to an RPi such as LEDs and push buttons in case that you
    don't have access to an RPi

    - **Ref:** `SimulRPi`_

`:star:`

   At the time of this writing (2020-08-28), I couldn't install ``pygame``
   1.9.6 (the latest stable release) with Python 3.5 and 3.8, on macOS.
   However, the latest pre-release development version (2.0.0.dev10) worked
   well with Python 3.5 and 3.8, on macOS.

.. _installation-instructions-label:

Installation instructions
=========================
.. TODO: IMPORTANT update released version in step 2
.. highlight:: none

1. It is highly recommended to install ``darth_vader_rpi`` in a virtual
   environment using for example `venv`_ or `conda`_.

2. Make sure to update *pip*::

   $ pip install --upgrade pip

3. Install the package ``darth_vader_rpi`` (released version **0.1.0a0**) with
   *pip*::

   $ pip install git+https://github.com/raul23/Darth-Vader-RPi@v0.1.0a0#egg=Darth-Vader-RPi

   It will install the dependencies if they are not already found in your system.

`:warning:`

   Make sure that *pip* is working with the correct Python version. It might be
   the case that *pip* is using Python 2.x You can find what Python version
   *pip* uses with the following::

      $ pip -V

   If *pip* is working with the wrong Python version, then try to use *pip3*
   which works with Python 3.x

`:information_source:`

   To install the **bleeding-edge version** of the ``darth_vader_rpi`` package::

      $ pip install git+https://github.com/raul23/Darth-Vader-RPi#egg=Darth-Vader-RPi

   However, this latest version is not as stable as the released version but you
   get the latest features being implemented.

**Warning message**

If you get the warning message from *pip* that the ``start_dv`` script is
not defined in your *PATH*::

      WARNING: The script start_dv is installed in '/home/pi/.local/bin' which is not on PATH.

Add the directory mentioned in the warning to your *PATH* by editing your
configuration file (e.g. *.bashrc*). See this `article`_ on how to set *PATH*
on Linux and macOS.

**Test installation**

1. Test your installation by importing ``darth_vader_rpi`` and printing its version::

   $ python -c "import darth_vader_rpi; print(darth_vader_rpi.__version__)"

2. You can also test that the dependencies were installed correctly::

   $ python -c "import dv_sounds, pygame, pynput, SimulRPi"

Usage
=====
Script ``start_dv``
-------------------
Once the ``darth_vader_rpi`` package is installed, you should have access to
the ``start_dv`` script which turns on LEDs and plays sound effects on a
Raspberry Pi (RPi).

Run the script on your **RPi** with `default values`_ for the GPIO channels
and other settings::

   $ start_dv

If you want to test the script on your **computer** (use the **-s** flag for
simulation)::

   $ start_dv -s

`:information_source:`

   Both previous commands will use the default values from the
   `configuration file`_ (e.g GPIO channel numbers, channel volume).

   Check `Change default settings`_ on how to modify these values.

`:star:`

   In order to stop the ``start_dv`` script at any moment, press
   ``ctrl`` + ``c``.

List of options
^^^^^^^^^^^^^^^
To display the script's list of options and their descriptions::

   $ start_dv -h

* ``--version``: show program's version number and exit
* ``-q, --quiet``: Enable quiet mode, i.e. nothing will be printed. (default: False)
* ``-s, --simulation``: Enable simulation mode, i.e. ``SimulRPi.GPIO`` will be used for simulating ``RPi.GPIO``. (default: False)
* ``-v, --verbose``: rint various debugging information, e.g. print traceback when there is an exception. (default: False)

Edit a configuration file:

* ``-e cfg_name, --edit cfg_name``: Edit a configuration file. Provide **log_cfg** for the logging 
  config file or **cfg** for the main config file. (default: None)

* ``-a APP, --app-name APP``: Name of the application to use for editing the file. If no name is 
  given, then the default application for opening this type of file will be used. (default: None)


Simulating on your computer
---------------------------
If you don't have access to a Raspberry Pi (RPi) and want to try out the
``start_dv`` script, you can run it with the **-s** flag. It will make use
of the `SimulRPi`_ library to simulate LEDs and push buttons connected to an
RPi by blinking red dots in the terminal and monitoring pressed keyboard keys::

   $ start_dv -s

**NOTE:** the last command makes use of default values. See
`Change default settings`_ on how to change these values.

Here's how the keyboard keys are related **by default** to push buttons
connected to an RPi:

* ``cmd_l``   -----> lightsaber button
* ``alt_l``   -----> song button
* ``alt_r``  -----> quotes button

Check `Change keymap`_ if you want to change this default key-to-channel
mapping.

Here is a video of what it looks like in a terminal when running the
``start_dv`` script on a computer instead of an RPi:

.. raw:: html

   <div align="center">
   <a href="https://youtu.be/NwVQlh5eu1g"><img src="https://img.youtube.com/vi/NwVQlh5eu1g/0.jpg"
   alt="LEDs and buttons simulation in a terminal [Darth-Vader-RPi project]"></a>
   <p><b>Click on the above image for the full video</b></p>
   </div>

How to uninstall
================
To uninstall **only** the package ``darth_vader_rpi``::

   $ pip uninstall darth_vader_rpi

To uninstall the package ``darth_vader_rpi`` and its dependencies::

   $ pip uninstall darth_vader_rpi dv_sounds pygame pynput simulrpi

You can exclude from the previous command-line those dependencies that you don't
want to uninstall.

`:information_source:`

   When uninstalling the ``darth_vader_rpi`` package, you might be informed
   that the configuration files *logging_cfg.json* and *main_cfg.json* won't be
   removed by *pip*. You can remove those files manually by noting their paths
   returned by *pip*. Or you can leave them so your saved settings can be
   re-used the next time you re-install the package.

   **Example:**

   .. code-block:: console

      $ pip uninstall darth-vader-rpi
      Found existing installation: Darth-Vader-RPi 0.1.0a0
      Uninstalling Darth-Vader-RPi-0.1.0a0:
        Would remove:
          /Users/test/miniconda3/envs/rpi_py37/bin/start_dv
          /Users/test/miniconda3/envs/rpi_py37/lib/python3.7/site-packages/Darth_Vader_RPi-0.1.0a0.dist-info/*
          /Users/test/miniconda3/envs/rpi_py37/lib/python3.7/site-packages/darth_vader_rpi/*
        Would not remove (might be manually added):
          /Users/test/miniconda3/envs/rpi_py37/lib/python3.7/site-packages/darth_vader_rpi/configs/logging_cfg.json
          /Users/test/miniconda3/envs/rpi_py37/lib/python3.7/site-packages/darth_vader_rpi/configs/main_cfg.json
      $ rm -r /Users/test/miniconda3/envs/rpi_py37/lib/python3.7/site-packages/darth_vader_rpi

Credits
=======
Sounds
------
- **Darth Vader quotes:**

  - `"I am your father" (YouTube)`_
  - `"Nooooo" (YouTube)`_
- **Music:**

  - `Imperial March song by Jacob Townsend`_ is licensed under a
    `Creative Commons (CC BY-NC-SA 3.0) License`_

    **NOTE:** The original song file was reduced under 1 MB by removing the
    first 7 seconds (no sound) and the last 2 minutes and 24 seconds.
- **Sound effects:**

  - `Darth Vader breathing sound (YouTube)`_
  - `Darth Vader's lightsaber sound effect (YouTube)`_
  - `Darth Vader's lightsaber retraction sound effect (YouTube)`_

Others
------
- **Schematic:**

  - `Scheme-it`_ from *Digi-Key Electronics* is an online schematic and
    diagramming tool that allows anyone to design and share electronic circuit
    diagrams.
- **Slot LEDs sequences:**

  - `Empire Strikes Back chest box light sequence (YouTube)`_

Resources
=========
* `Darth-Vader-RPi documentation`_
* `Darth-Vader-RPi Changelog`_


References
==========
* `dv_sounds`_: a package for downloading the various sounds needed for the
  ``Darth-Vader-RPi`` project, e.g. ligthsaber sound effects.
* `pygame`_: a Python library to write multimedia software, such as games,
  built on top of the SDL library.
* `RPI.GPIO`_: a module to control RPi GPIO channels.
* `SimulRPi`_: a package that partly fakes ``RPi.GPIO`` and simulates some I/O
  devices on a Raspberry Pi. It makes use of the `pynput`_ library for
  monitoring the keyboard for any pressed key.

.. URLs

.. 0. default_main_cfg
.. _as specified in the configuration file:
   https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L51
.. _configuration file: https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L1
.. _default values: https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L1

.. 1. External links (darth-vader-rpi.readthedocs.io)
.. _add more quotes: https://darth-vader-rpi.readthedocs.io/en/v0.1.0a0/change_default_settings.html#add-darth-vader-quotes-label
.. _closing sound: https://darth-vader-rpi.readthedocs.io/en/v0.1.0a0/change_default_settings.html#change-closing-sound-label
.. _Change default settings: https://darth-vader-rpi.readthedocs.io/en/v0.1.0a0/change_default_settings.html
.. _Change keymap: https://darth-vader-rpi.readthedocs.io/en/v0.1.0a0/change_default_settings.html#change-keymap-label
.. _Darth-Vader-RPi Changelog: https://darth-vader-rpi.readthedocs.io/en/latest/changelog.html

.. 2. External links (others)
.. _article: https://docs.oracle.com/cd/E19062-01/sun.mgmt.ctr36/819-5418/gaznb/index.html
.. _conda: https://docs.conda.io/en/latest/
.. _dv_sounds: https://github.com/raul23/DV-Sounds
.. _pygame: https://www.pygame.org/
.. _pynput: https://pynput.readthedocs.io
.. _this one from Hasbro: https://amzn.to/3hIw0ou
.. _venv: https://docs.python.org/3/library/venv.html#module-venv
.. _Darth-Vader-RPi documentation: http://darth-vader-rpi.rtfd.io/
.. _"I am your father" (YouTube): https://www.youtube.com/watch?v=xuJEYdOFEP4
.. _Creative Commons (CC BY-NC-SA 3.0) License: http://creativecommons.org/licenses/by-nc-sa/3.0/
.. _Darth Vader breathing sound (YouTube): https://www.youtube.com/watch?v=d28NrjMPERs
.. _Darth Vader's lightsaber retraction sound effect (YouTube): https://www.youtube.com/watch?v=m6buyGJF46k
.. _Darth Vader's lightsaber sound effect (YouTube): https://www.youtube.com/watch?v=bord-573NWY
.. _Empire Strikes Back chest box light sequence (YouTube): https://youtu.be/E2J_xl2MbGU?t=333
.. _Imperial March song by Jacob Townsend: https://soundcloud.com/jacobtownsend1/imperial-march
.. _"Nooooo" (YouTube): https://www.youtube.com/watch?v=ZscVhFvD6iE
.. _RPi.GPIO: https://pypi.org/project/RPi.GPIO/
.. _Scheme-it: https://www.digikey.com/en/resources/design-tools/schemeit
.. _SimulRPi: https://pypi.org/project/SimulRPi/
