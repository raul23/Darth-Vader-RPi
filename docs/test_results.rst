=============================
Test results for ``start_dv``
=============================
We will present how the script ``start_dv`` performed on various platforms and
environments based on different releases of the package ``darth_vader_rpi``.

**IMPORTANT:** when uninstalling only ``SimulRPi`` with:: 

   $ pip uninstall simulrpi

And then installing it with::
   
   $ pip install git+https://github.com/raul23/Darth-Vader-RPi#egg=Darth-Vader-RPi

You will get ``SimulRPi`` from PyPI instead of the bleeding-edge version from github. Thus,
you might get an old version of ``SimulRPi`` if you haven't yet published the latest version
to PyPI.

.. contents::
   :depth: 3
   :local:

``darth_vader_rpi`` v0.1.0a0
============================
Raspberry Pi (Python 3.5)
^^^^^^^^^^^^^^^^^^^^^^^^^

with ``RPi.GPIO``
"""""""""""""""""
**TODO**

with ``SimulRPi.GPIO``
""""""""""""""""""""""
**TODO**

macOS
^^^^^

Python 3.5
""""""""""
**Dependencies installed:**

* **IMPORTANT:** Install ``pygame`` first with ``pip install pygame==2.0.0.dev10``
* ``dv_sounds 0.1.0a0``
* ``pygame 2.0.0.dev10``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

The command ``start_dv -s`` gives this error::

   ERROR    UnicodeEncodeError: 'ascii' codec can't encode character '\U0001f6d1' in position 2: ordinal not in range(128)

This error stems from my locale settings which are not set properly and it
seems that Python 3.5 doesn't assume the correct locale *utf-8* by default.
Check `Display problems`_ on how to set the locale settings correctly.

**Result:** once the locale settings are setup correctly, the command
``start_dv -s`` runs without errors.

Python 3.6
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

Same ``UnicodeEncodeError`` as in Python 3.5 Set my local settings correctly
and the script runs fine.

**Result:** once the locale settings are setup correctly, the command
``start_dv -s`` runs without errors.

Python 3.7
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the command ``start_dv -s`` runs without errors.

Python 3.8
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 2.0.0.dev10``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the command ``start_dv -s`` runs without errors.

SSH from macOS to RPi (Python 3.5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Dependencies installed on the RPi (Python 3.5):**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.3``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

As expected ``pynput`` could not be imported because it doesn't work on a
headless setup (connecting to an RPi via SSH). However, the blinking of slot
LEDs on the Darth Vader figurine or in the terminal works.

**Result 1:** the command ``start_dv`` runs without errors. Blinking of slot
LEDs on the Darth Vader figurine works and the push button turns on and off the
lightsaber.

**Result 2:** the command ``start_dv -s`` runs without errors, except a warning
about ``pynput`` not being able to be imported. Blinking of slot LEDs in the
terminal works.

.. URLs
.. external links
.. _Display problems: https://simulrpi.readthedocs.io/en/latest/display_problems.html#non-ascii-characters-can-t-be-displayed
