=============================
Test results for ``start_dv``
=============================
We will present how the ``start_dv`` script performed on various platforms and
environments based on different releases of the ``darth_vader_rpi`` package.

.. contents:: **Contents**
   :depth: 3
   :local:

Important tips
==============
Tip: careful when uninstalling only ``SimulRPi``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When uninstalling **only** ``SimulRPi`` with::

   $ pip uninstall simulrpi

And then installing it with::

   $ pip install git+https://github.com/raul23/Darth-Vader-RPi#egg=Darth-Vader-RPi

You will get ``SimulRPi`` from PyPI instead of the bleeding-edge version from
github even though ``requirements.txt`` points to ``SimulRPi`` from github.

Thus, you might get an old version of ``SimulRPi`` if you haven't yet
published the latest version to PyPI. In the latter case, it is then preferable
to uninstall all modules if you want the ``SimulRPi`` version from github.

Tip: use ``pip3`` when working with RPi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When doing tests on the RPi's Debian OS, use ``pip3`` because ``pip`` points to
Python 2.7

``darth_vader_rpi`` v0.1.0a0
============================

macOS
^^^^^

Python 3.5
""""""""""
**IMPORTANT:** Install ``pygame`` first with:: 

   $ pip install pygame==2.0.0.dev10

**Dependencies installed:**

* ``pygame 2.0.0.dev10``
* ``dv_sounds 0.1.0a0``
* ``pygame 2.0.0.dev10``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

The ``$ start_dv -s`` command gives this error::

   ERROR    UnicodeEncodeError: 'ascii' codec can't encode character '\U0001f6d1' in position 2: ordinal not in range(128)

This error stems from the locale settings which are not set properly and it
seems that Python 3.5 doesn't assume the correct *utf-8* encoding by default.
Check `Display problems`_ on how to set the locale settings correctly.

**Result:** once the locale settings are setup correctly, the
``$ start_dv -s`` command runs without errors.

Python 3.6
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

Same ``UnicodeEncodeError`` as in Python 3.5 Set the local settings correctly
and the script runs fine.

**Result:** once the locale settings are setup correctly, the
``$ start_dv -s`` command runs without errors.

Python 3.7
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the ``$ start_dv -s`` command runs without errors.

Python 3.8
""""""""""
**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 2.0.0.dev10``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the ``$ start_dv -s`` command runs without errors.

Raspberry Pi (Python 3.5)
^^^^^^^^^^^^^^^^^^^^^^^^^

with ``RPi.GPIO``
"""""""""""""""""
**IMPORTANT:** Use ``pip3`` since ``pip`` points to Python 2.7

**Dependencies installed on the RPi (Python 3.5):**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.3`` (already installed with the OS and **don't uninstall it!**)
* ``pynput 1.7.1``
* ``RPi.GPIO``

**Result:** the ``$ start_dv`` command runs without errors.

* Blinking of slot LEDs on the Darth Vader figurine works.
* When pressed, the push buttons produce the different sounds (lightsaber
  sounds, Darth Vader's theme song and quotes) and turns on and off the
  lightsaber.

with ``SimulRPi.GPIO``
""""""""""""""""""""""
**IMPORTANT:** Use ``pip3`` since ``pip`` points to Python 2.7

**Dependencies installed on the RPi (Python 3.5):**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.3`` (already installed with the OS and **don't uninstall it!**)
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

Couldn't display the default non-ASCII LED symbols even though the two
solutions in `Display problems`_ were tried. Finally, ASCII LED symbols were
used by setting ``default_led_symbols`` to ``"default_ascii"`` in the main
configuration file as explained in the same article
`Display problems (Use ASCII-based LED symbols)`_.

**Result:** the ``$ start_dv -s`` command runs without errors.

* Blinking of slot LEDs and illumination of the lightsaber in the terminal works.
* When pressed, the valid keyboard keys produce the different sounds:
  lightsaber sounds, Darth Vader's theme song and quotes.

SSH from macOS to RPi (Python 3.5)
""""""""""""""""""""""""""""""""""
**IMPORTANT:** Use ``pip3`` since ``pip`` points to Python 2.7

**Dependencies installed on the RPi (Python 3.5):**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.3`` (already installed with the OS and **don't uninstall it!**)
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

As expected ``pynput`` could not be imported because it doesn't work on a
headless setup (connecting to an RPi via SSH). However, the blinking of slot
LEDs on the Darth Vader figurine or in the terminal works.

**Result 1:** the ``$ start_dv`` command runs without errors.

* Blinking of slot LEDs on the Darth Vader figurine works.
* The push button turns on and off the lightsaber.

**Result 2:** the ``$ start_dv -s`` command runs without errors

* Warning about ``pynput`` not being able to be imported (expected)
* Blinking of slot LEDs in the terminal works.

.. URLs
.. external links
.. _Display problems: https://simulrpi.readthedocs.io/en/latest/display_problems.html#non-ascii-characters-can-t-be-displayed
.. _Display problems (Use ASCII-based LED symbols): https://simulrpi.readthedocs.io/en/latest/display_problems.html#use-ascii-based-led-symbols