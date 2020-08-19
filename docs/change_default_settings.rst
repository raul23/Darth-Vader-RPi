.. _configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _logging configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_logging_cfg.json
.. _main configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json
.. _setting GPIO_channels: #change-gpio-channels
.. _"I am your father": https://www.youtube.com/watch?v=xuJEYdOFEP4
.. _"Nooooo": https://www.youtube.com/watch?v=ZscVhFvD6iE
.. _Platform limitations: https://simulrpi.readthedocs.io/en/latest/api_reference.html#important-platform-limitations-label
.. _SimulRPi's documentation: https://simulrpi.readthedocs.io/en/latest/api_reference.html#content-default-keymap-label

=======================
Change default settings
=======================

.. contents::
   :depth: 2
   :local:

Introduction
============

The default settings used by the script ``start_dv`` are found in the
`main configuration file`_. It is referred to as *main* because there is another
config file you could edit, the `logging configuration file`_.

The *main* configuration file can be edited with the following command::

   $ start_dv -e cfg

The logging configuration file could be instead edited with the `-e log_cfg`
command-line option.

This will open the configuration file with the default text editor that is
associated with JSON files as specified in your system, e.g. *atom* on macOS or
*vim* on Linux.

If you want to use another text editor you can specify it with the `-a APP`
command-line option::

   $ start_dv -e cfg -a TextEdit

Add Darth Vader quotes
======================
The script ``start_dv`` comes included with two movie lines:

   * `"I am your father"`_
   * `"Nooooo"`_

If you want to add more Darth Vader quotes, you have to edit the setting
``quotes`` in the configuration file. Open the configuration file with::

   $ start_dv -e cfg

Change channel volume
=====================

Change GPIO channels
====================

Change keymap
=============
.. TODO: check line numbers before publishing

If you want to change the default keymap, edit the setting
``key_to_channel_map`` in the `configuration file <https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L18>`__
which can be opened with::

   $ start_dv -e cfg

.. literalinclude:: ../darth_vader_rpi/configs/default_main_cfg.json
   :language: python
   :lines: 18-23
   :emphasize-lines: 3-5
   :caption: **Default keymap used in the configuration file**

You will need to change the name of the keyboard key.

The names of keyboard keys that you can use are those specified in the
`SimulRPi's documentation`_, e.g. `media_play_pause`, `shift`, and `shift_r`.

The value for each keyboard key is the GPIO channel number (integer) associated
with a push button, e.g. 23 is related to the *ligthsaber_button*. The GPIO
channels are identified in the `setting GPIO_channels`_ from the configuration
file.

.. note::

   On mac, I recommend using the following keyboard keys because they don't
   require running the script ``start_dv`` with ``sudo``: *alt*, *alt_r*,
   *cmd*, *cmd_r*, *ctrl*, *ctrl_r*, *media_play_pause*,
   *media_volume_down*, *media_volume_mute*, *media_volume_up*, *shift*,
   and *shift_r*.

   **Ref.:** `Platform limitations`_

Change paths to audio files
===========================

Change slot LEDs sequence
=========================

Mute breathing and closing sounds
=================================
