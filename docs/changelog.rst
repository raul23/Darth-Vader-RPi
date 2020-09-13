=========
Changelog
=========

Version 0.1.0a0
===============
.. TODO: IMPORTANT add date

**September 13, 2020**

* Initial release
* Tested the script :mod:`start_dv` on various platforms and environments.

  **Here are the results:**

  * Raspberry Pi (Python 3.5): **TODO**

  * macOS:

    * The command ``start_dv -s`` runs without errors on Python 3.7 and 3.8

    * On Python 3.5 and 3.6, I had to set my locale settings to
      ``LANG="en_US.UTF-8"`` to make the command ``start_dv -s`` work. Thus, it
      was not an error with the script but with how my system environment was
      setup. Python 3.5 and 3.6 don't assume an **UTF-8** based local settings
      like the other more recent Python versions.

  * SSH from macOS to RPi (Python 3.5):

    * Running the command ``start_dv`` runs without errors.

    * Running the command ``start_dv -s` with produces a warning about
      ``pynput`` not being able to be imported (as expected) but the rest of
      the code that doesn't depend on keyboard keys being detected works, i.e.
      blinking of LED symbols in the terminal.

  .. note::

    For more detailed information about these tests, check
    `Test results for start_dv`_


.. URLs
.. external links
.. _Test results for start_dv: https://github.com/raul23/Darth-Vader-RPi/blob/master/docs/test_results.rst
