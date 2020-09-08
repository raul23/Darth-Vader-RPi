=========
Changelog
=========

Version 0.1.0a0
===============
.. TODO: IMPORTANT add date

**September 8, 2020**

* Initial release
* Tested the script :mod:`start_dv` on various platforms and environments.

  **Here are the results:**

  * Raspberry Pi (Python 3.5): **TODO**

  * macOS:

    * The script :mod:`start_dv` runs without errors on Python 3.6-3.8

    * On Python 3.5, I had to fix my locale settings to ``LANG="en_US.UTF-8"``
      to make the script :mod:`start_dv` works. Thus, it was not an error with
      the script per se but with how my environment was setup. Python 3.5
      doesn't assume an **UTF-8** based local settings like the other more
      recent Python versions.

  * SSH from macOS to RPi: **TODO**

  .. note::

    For more detailed information about these tests, check
    `Test results for start_dv`_

.. URLs
.. external_links
.. _Test results for start_dv: https://github.com/raul23/Darth-Vader-RPi/blob/master/docs/test_results.rst
