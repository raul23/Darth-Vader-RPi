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

**Darth-Vader-RPi** (|version|) is a Python-based Raspberry Pi (RPi) project about
activating a Darth Vader action figure by turning on LEDs on his suit and
lightsaber, and by playing sounds such as some of his famous quotes.

.. important::

   If you don't have an RPi, don't worry. You can still
   `test the program on your own computer`_ because the package
   ``darth_vader_rpi`` uses the library `SimulRPi`_ to simulate I/O devices
   connected to an RPi such as LEDs and push buttons by blinking red dots in
   the terminal and playing sounds when a keyboard key is pressed. Almost like
   testing with a real RPi!

   **Disclaimer:** I also wrote the library `SimulRPi`_

.. contents:: **Table of contents**
   :depth: 3
   :local:

Introduction
============
The Darth Vader action figure is 11.5 inches tall (which is
`this one from Hasbro`_) and was modified to make it more lifelike by
illuminating the lightsaber, chest control box, and belt. 3 push buttons
control the following sounds and LEDs:

#. Some of his famous quotes
#. The *Imperial march* theme song
#. The lightsaber drawing, hum and retraction sounds
#. The lightbsaber illumination (3 LEDs)

His iconic breathing sound plays in the background indefinitely almost as soon
as the RPi is run with the script `start_dv`_.

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

* The lightsaber is illuminated by 3 LEDs connected in parallel
* The *Top*, *Middle*, and *Bottom* LEDs illuminate the slots in Darth Vader's
  chest control box. They blink in a specific sequence
  `as specified in the configuration file`_.
* When the *Lightsaber button* is first pressed, it produces the drawing sound,
  illuminates the sword, and a hum sound persists until the *Lightsaber button*
  is turned off. If the button is pressed again, it produces the sound of
  retracting the lightsaber and turns it off.

  **NOTE:** the *Lightsaber button* can be pressed while the *Song button* or
  the *Quotes button* is playing audio since they use different audio channels.
* The *Song button* plays the `Imperial March song by Jacob Townsend`_
* The *Quotes button* plays famous Darth Vader quotes when pressed. For
  testing purposes, the package ``darth_vader_rpi`` comes with two movie lines:

  * `"I am your father"`_
  * `"Nooooo"`_: it is also used for the `closing sound`_ when the script
    `start_dv`_ exits

  However, you could `add more quotes`_ if you want.

Dependencies
============
* **Platforms:** macOS, Linux
* **Python**: 3.5, 3.6, 3.7, 3.8
* **Packages**

  * ``dv_sounds``>=0.1.0a0: for retrieving the sound files (quotes, songs, and
    sound effects)

    - **Ref:** `dv_sounds`_
  * ``pygame``>=1.9.3: for playing sounds

    - **Ref:** `pygame`_
  * ``pynput``>=1.6.8: needed by ``SimulRPi`` for monitoring the keyboard when
    simulating push buttons with keyboard keys, i.e. when running the script
    `start_dv`_ in simulation mode

    - **Ref:** `pynput`_
  * ``SimulRPi`` >=0.1.0a0: for partly faking `RPI.GPIO`_ and simulating I/O
    devices connected to an RPi such as LEDs and push buttons in case that you
    don't have access to an RPi

    - **Ref:** `SimulRPi`_

.. important::

   At the time of this writing (2020-08-28), I couldn't install ``pygame``
   1.9.6 (the latest stable release) with Python 3.5 and 3.8, on macOS.
   However, the latest pre-release development version (2.0.0.dev10) worked
   well with Python 3.5 and 3.8, on macOS.

.. _installation-instructions-label:

Installation instructions
=========================
.. TODO: IMPORTANT modify SimulRPi in requirements.txt to point to pypi
.. highlight:: none

1. Make sure to update pip::

   $ pip install --upgrade pip

2. Install the package ``darth_vader_rpi`` with *pip*::

   $ pip install git+https://github.com/raul23/Darth-Vader-RPi#egg=Darth-Vader-RPi

   It will install the dependencies if they are not already found in your system.

.. important::

   Make sure that *pip* is working with the correct Python version. It might be
   the case that *pip* is using Python 2.x You can find what Python version
   *pip* uses with the following::

      $ pip -V

   If *pip* is working with the wrong Python version, then try to use *pip3*
   which works with Python 3.x

**Test installation**

1. Test your installation by importing ``darth_vader_rpi`` and printing its version::

   $ python -c "import darth_vader_rpi; print(darth_vader_rpi.__version__)"

2. You can also test that the dependencies were installed correctly::

   $ python -c "import dv_sounds, pygame, pynput, SimulRPi"

**Warning message**

If you get the warning message from *pip* that the script :mod:`start_dv` is
not defined in your *PATH*::

      WARNING: The script start_dv is installed in '/home/pi/.local/bin' which is not on PATH.

Add the directory mentioned in the warning to your *PATH* by editing your
configuration file (e.g. *.bashrc*). See this `article`_ on how to set *PATH*
on Linux.

Usage
=====
Script ``start_dv``
-------------------
Once the package ``darth_vader_rpi`` is `installed`_, you should have access to
the script :mod:`start_dv` which turns on LEDs and plays sound effects on a
Raspberry Pi (RPi).

Run the script on your **RPi** with `default values`_ for the GPIO channels
and other settings::

   $ start_dv

If you want to test the script on your **computer** (use the flag **-s**)::

   $ start_dv -s

.. note::

   Both previous commands will use the default values from the
   `configuration file`_ (e.g GPIO channel numbers, channel volume).

   Check `Change default settings`_ on how to modify these values.

.. important::

   In order to stop the script :mod:`start_dv` at any moment, press
   ``ctrl`` + ``c``.

List of options
^^^^^^^^^^^^^^^
To display the script's list of options and their descriptions:
``$ start_dv -h``

--version            show program's version number and exit
-q, --quiet          Enable quiet mode, i.e. nothing will be printed.
                     (default: False)
-s, --simulation     Enable simulation mode, i.e. ``SimulRPi.GPIO`` will be
                     used for simulating ``RPi.GPIO``. (default: False)
-v, --verbose        Print various debugging information, e.g. print
                     traceback when there is an exception. (default: False)

Edit a configuration file:

-e cfg_name, --edit cfg_name   Edit a configuration file. Provide **log_cfg**
                               for the logging config file or **cfg** for the
                               main config file. (default: None)

-a APP, --app-name APP   Name of the application to use for editing the file.
                         If no name is given, then the default application for
                         opening this type of file will be used. (default:
                         None)


Simulating on your computer
---------------------------
If you don't have access to a Raspberry Pi (RPi) and want to try out the script
:mod:`start_dv`, you can run the script with the flag **-s**. It will make use
of the library `SimulRPi`_ to simulate LEDs and push buttons connected to an
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

Here is a video of what it looks like in a terminal when running the script
:mod:`start_dv` on a computer instead of an RPi:

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

You can remove from the previous command-line those dependencies that you don't
want to uninstall.

.. note::

   When uninstalling the package ``darth_vader_rpi``, you might be informed
   that the configuration files *logging_cfg.json* and *main_cfg.json* won't be
   removed by *pip*. You can remove those files manually by noting their paths
   returned by *pip*. Or you can leave them so your saved settings can be
   re-used the next time you re-install the package.

   **Example:**

   .. code-block:: console
      :emphasize-lines: 8, 11

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
- **Darth Vader quotes:**

  - `"I am your father"`_
  - `"Nooooo"`_
- **Music:**

  - `Imperial March song by Jacob Townsend`_ is licensed under a
    `Creative Commons (CC BY-NC-SA 3.0) License`_

    **NOTE:** The original song file was reduced under 1 MB by removing the
    first 7 seconds (no sound) and the last 2 minutes and 24 seconds.
- **Sound effects:**

  - `Darth Vader breathing sound`_
  - `Darth Vader's lightsaber sound effect`_
  - `Darth Vader's lightsaber retraction sound effect`_
- **Slot LEDs sequences:**

  - `Empire Strikes Back chest box light sequence`_

Resources
=========
* `Darth-Vader-RPi GitHub`_: source code


References
==========
* `dv_sounds`_: a package for downloading the various sounds needed for the
  project, e.g. sound effects
* `pygame`_: a package used for playing sounds
* `RPI.GPIO`_: a module to control RPi GPIO channels
* `SimulRPi`_: a package that partly fakes ``RPi.GPIO`` and simulates some I/O
  devices on a Raspberry Pi. It makes use of the library `pynput`_ for
  monitoring the keyboard for any pressed key.

.. URLs

.. 0. default_main_cfg
.. _as specified in the configuration file:
   https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L51
.. _configuration file: https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L1
.. _default values: https://github.com/raul23/archive/blob/master/SimulRPi/v0.1.0a0/default_main_cfg.json#L1

.. 1. External links
.. _article: https://docs.oracle.com/cd/E19062-01/sun.mgmt.ctr36/819-5418/gaznb/index.html
.. _dv_sounds: https://github.com/raul23/DV-Sounds
.. _pygame: https://www.pygame.org/
.. _pynput: https://pynput.readthedocs.io
.. _this one from Hasbro: https://amzn.to/3hIw0ou
.. _Darth-Vader-RPi GitHub: https://github.com/raul23/Darth-Vader-RPi
.. _"I am your father": https://www.youtube.com/watch?v=xuJEYdOFEP4
.. _Creative Commons (CC BY-NC-SA 3.0) License: http://creativecommons.org/licenses/by-nc-sa/3.0/
.. _Darth Vader breathing sound: https://www.youtube.com/watch?v=d28NrjMPERs
.. _Darth Vader's lightsaber retraction sound effect: https://www.youtube.com/watch?v=m6buyGJF46k
.. _Darth Vader's lightsaber sound effect: https://www.youtube.com/watch?v=bord-573NWY
.. _Empire Strikes Back chest box light sequence: https://youtu.be/E2J_xl2MbGU?t=333
.. _Imperial March song by Jacob Townsend: https://soundcloud.com/jacobtownsend1/imperial-march
.. _"Nooooo": https://www.youtube.com/watch?v=ZscVhFvD6iE
.. _RPi.GPIO: https://pypi.org/project/RPi.GPIO/
.. _SimulRPi: https://pypi.org/project/SimulRPi/

.. 2. Internal links
.. _add more quotes: change_default_settings.html#add-darth-vader-quotes-label
.. _closing sound: change_default_settings.html#change-closing-sound-label
.. _installed: #installation-instructions-label
.. _start_dv: #script-start-dv
.. _test the program on your own computer: #simulating-on-your-computer
.. _Change default settings: change_default_settings.html
.. _Change keymap: change_default_settings.html#change-keymap-label
.. _Darth-Vader-RPi Changelog: changelog.html
