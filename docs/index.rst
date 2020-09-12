Darth-Vader-RPi's documentation
===============================

.. raw:: html

   <p align="center"><img src=_static/images/Darth_Vader_RPi_logo.png>
   <br> 🚧 &nbsp;&nbsp;&nbsp;<b>Work-In-Progress</b>
   </p>

**Darth-Vader-RPi** is a Python-based Raspberry Pi project about activating a Darth Vader
action figure by turning on LEDs on his suit and lightsaber, and by playing
sounds such as some of his famous quotes. See the `README <README_docs.html>`_ for
more info about the project.

.. raw:: html

   <div align="center">
   <a href="https://www.youtube.com/embed/P631S1k1h_0">
   <img src="https://raw.githubusercontent.com/raul23/images/master/Darth-Vader-RPi/darth_vader_lightsaber_2x_speed_smaller_version.gif"/>
   </a>
   <p><b>Turning on/off the lightsaber</b></p>
   </div>

..
   important::

   If you don't have an RPi, don't worry. You can still test the program on
   your own computer because the package ``darth_vader_rpi`` uses the library
   `SimulRPi`_ to simulate I/O devices connected to an RPi such as LEDs and
   push buttons by blinking red dots in the terminal and playing sounds when a
   keyboard key is pressed. Almost like testing with a real RPi!

   **Disclaimer:** I also wrote the `SimulRPi`_ library

.. TODO: this important notice is also found in README.rst

.. toctree::
   :maxdepth: 1
   :caption: Contents

   README_docs
   main_config
   change_default_settings
   api_reference
   changelog
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
