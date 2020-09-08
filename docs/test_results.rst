=============================
Test results for ``start_dv``
=============================

I present how the script ``start_dv`` performed on various platforms and
environments based on different releases of the library ``Darth-Vader-RPi``.

.. contents::
   :depth: 3
   :local:

Version 0.1.0a0
===============
Raspberry Pi (Python 3.5)
^^^^^^^^^^^^^^^^^^^^^^^^^

with ``RPi.GPIO``
"""""""""""""""""

with ``SimulRPi.GPIO``
""""""""""""""""""""""

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

This error stems from my locale settings which are not set properly. Check
`Display problems`_ on how to set them.

Once the locale setting is setup correctly, the script ``start_dv -s`` runs
without errors.

Python 3.6
""""""""""

Python 3.7
""""""""""

Python 3.8
""""""""""

SSH from macOS to RPi
^^^^^^^^^^^^^^^^^^^^^

.. URLs
.. external links
.. _Display problems: https://simulrpi.readthedocs.io/en/latest/display_problems.html#solution-1-change-your-locale-settings
