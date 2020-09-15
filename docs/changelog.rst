=========
Changelog
=========

Version 0.1.0a0
===============
**September 15, 2020**

* Initial release
* Tested the :mod:`start_dv` script on various platforms and environments.

  **Here are the results:**

  * macOS:

    * The ``start_dv -s`` command runs without errors on Python 3.7 and 3.8

    * On Python 3.5 and 3.6, I had to set my locale settings to
      ``LANG="en_US.UTF-8"`` to make the ``start_dv -s`` command work. Thus,
      it was not an error with the script but with how my system environment
      was setup. Python 3.5 and 3.6 don't assume an **UTF-8** based local
      settings like the other more recent Python versions.

  * Raspberry Pi (Python 3.5):

    * Running the ``start_dv`` command without errors.
    * Running the ``start_dv -s`` command without errors.

  * SSH from macOS to RPi (Python 3.5):

    * Running the ``start_dv`` command without errors.

    * Running the ``start_dv -s`` command produces a warning about ``pynput``
      not being able to be imported (as expected) but the rest of the code that
      doesn't depend on keyboard keys being detected works, i.e. blinking of
      LED symbols in the terminal.

  .. note::

    For more detailed information about these tests, check
    `Test results for start_dv`_


.. URLs
.. external links
.. _Test results for start_dv: https://github.com/raul23/Darth-Vader-RPi/blob/master/docs/test_results.rst#darth-vader-rpi-v0-1-0a0
