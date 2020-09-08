=============================
Test results for ``start_dv``
=============================

I present how the script ``start_dv`` performed on various platforms and
environments based on different releases of the package ``darth_vader_rpi``.

.. contents::
   :depth: 3
   :local:

Version 0.1.0a0
===============
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

The script ``start_dv -s`` gives this error::

   ERROR    UnicodeEncodeError: 'ascii' codec can't encode character '\U0001f6d1' in position 2: ordinal not in range(128)

This error stems from my locale settings which are not set properly and it
seems that Python 3.5 doesn't assume the correct locale *utf-8* by default.
Check `Display problems`_ on how to set the locale settings correctly.

**Result:** once the locale settings are setup correctly, the script
``start_dv -s`` runs without errors.

Python 3.6
""""""""""

**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the script ``start_dv -s`` runs without errors.

Python 3.7
""""""""""

**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 1.9.6``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the script ``start_dv -s`` runs without errors.

Python 3.8
""""""""""

**Dependencies installed:**

* ``dv_sounds 0.1.0a0``
* ``pygame 2.0.0.dev10``
* ``pynput 1.7.1``
* ``SimulRPi 0.1.0a0``

**Result:** the script ``start_dv -s`` runs without errors.

SSH from macOS to RPi (Python 3.5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**TODO**

.. URLs
.. external links
.. _Display problems: https://simulrpi.readthedocs.io/en/latest/display_problems.html#solution-1-change-your-locale-settings
