.. Darth-Vader-RPi documentation master file, created by
   sphinx-quickstart on Sat Jul 25 03:43:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _SimulRPi: https://simulrpi.readthedocs.io/en/latest/

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
   <img src="https://lh3.googleusercontent.com/nIDDvKensOS1XhwQkTRacdY9sFHRPAU_pxpviT4lzx74euAXPoxBbeJTVxks7YgzTGd5PIJ1oAQUobujrt81TBiL-11axbDV-RlZmhRP1tMSct3mnAv-NdFbmgGgs4GZBp-FKeFhTNACl_zI6r9-EvViYdSFvYOiLXTQHUks9xfKBbUi4xJrEjHyiDx8NgrlLW3Jox0Y639gVXzQKVO8vEkvgvmdzz6XgDutOZlyC2i1VlVhsv7hZAyBC4qZ7UpIYLlj0m5-kaFRBvbzr0aj_jprLn0xp_lRhtPFZzXu7O8LnOUNgVRr4qNW_gMbhPkXfD40n5XkxP2DwegVBukpd4Om_R8H0cBtmL0Oahprf6in8Exlyg5yDAZYcUjHlKxRswHpS2lRancihqpz6I36VtZI9a_vSZyAK0ce-Y2DTO05j4OwQX5QKvzyGk-H6hVnNeVzVaLHOgVa2cFFReEdR1Xd-eHTH5rwBIs41K1Sj3gXv9LFV5WoWlgCPvKR_1HqwBWWwT__7M5-J6Xh6Y7aDjKLZK3sDB5GNWmqHZXebc_Jwi-iPwvyOJ55tvdPk-dfS6BpFF-nShIjS7oaIc6THZC8nKPgraJb1c-b2_pkclfS4UQYxFZzEg7wBtHCicTX95YjuReHU3jl_YluQrgBdf-BjHRfggGW6b5wvobPKpU2FtP0BxVTHHwOjXBL=w338-h450-no?authuser=0"/>
   <p><b>Turning on/off the lightsaber</b></p>
   </div>

..
   important::

   If you don't have an RPi, don't worry. You can still test the program on
   your own computer because the package ``darth_vader_rpi`` uses the library
   `SimulRPi`_ to simulate I/O devices connected to an RPi such as LEDs and
   push buttons by blinking small circles on the terminal and playing sounds
   when a keyboard key is pressed. Almost like testing with a real RPi!

   **Disclaimer:** I also wrote the `SimulRPi`_ library

.. TODO: this important notice is also found in README.rst

.. toctree::
   :maxdepth: 1
   :caption: Contents

   README_docs
   change_default_settings
   api_reference
   changelog
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
