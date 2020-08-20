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

Important tips
==============
- When adding audio files, use *ogg* (compressed) or *wav* (uncompressed) as the
  file format. The reason is that other file formats like *mp3* won't work
  well with pygame's simultaneous playback capability.

  **Reference:** `stackoverflow <https://stackoverflow.com/a/59742418>`__
- 

Add Darth Vader quotes
======================
The script ``start_dv`` comes included with two movie lines:

   - `"I am your father"`_
   - `"Nooooo"`_

.. TODO: check line in URL to config file showing ``quotes``

Quotes are represented in the `configuration file <https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L86>`__
as objects having the following properties:

   - ``name``: will be displayed in the terminal
   - ``filename``: relative to the directory ``sounds_directory``
   - ``audio_channel_id``: all quotes should be played in **channel 1** as
     explained in `Change channel volume <#change-channel-volume>`__

If you want to add more Darth Vader quotes, you have to edit the setting
``quotes`` in the configuration file. Open the configuration file with::

   $ start_dv -e cfg

Add your object representing the quote to the list in ``quotes``, like in the
following example:

.. code-block:: python
   :emphasize-lines: 2-6
   :caption: **Example:** adding a new quote

   "quotes": [
     {
       "name": "there_is_no_escape",
       "filename": "quote_there_is_no_escape.ogg",
       "audio_channel_id": 1
     }
   ]

Change channel volume
=====================
Three channels are used for this project:

   - **channel 0**: used for the breathing sound which plays in the background
     as soon as the script runs. Its volume is set by default at 0.2 since we
     don't want to overwhelm the other sounds playing in the other channels.
   - **channel 1**: used for playing the *Imperial March* song and all Darth
     Vader quotes.  Its volume is set by default at 1.0
   - **channel 2**: used for playing the lighsaber sound effects and the closing
     sound. Its volume is set by default at 1.0

To change the volume for an audio channel, open the configuration file and edit
the channel's volume found in the setting ``audio_channels``::

   $ start_dv -e cfg

.. code-block:: python
   :emphasize-lines: 4, 8, 12
   :caption: **Audio channels and their default volumes**

   "audio_channels": [
     {
       "audio_channel_id": 0,
       "volume": 0.2
     },
     {
       "audio_channel_id": 1,
       "volume": 1.0
     },
     {
       "audio_channel_id": 2,
       "volume": 1.0
     }
   ],

.. note::

   Volume takes values in the range 0.0 to 1.0 (inclusive). As per the `pygame's
   documentation <https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.set_volume>`__.

Change closing sound
====================
When the script is exitng after the user presses ``ctrl`` + ``c``, a sound is
produced which by default is the `"Nooooo"`_ quote.

To change the default closing sound, edit the setting ``sound_effects`` in the
configuration file which can be opened with::

   $ start_dv -e cfg

At the end of the list in ``sound_effects``, you will find the ``closing_sound``
object. These are the properties you can modify:

   - ``filename``: relative to ``sound_directory``
   - ``play_closing``: if `true`, the closing sound will be played when the
     script is finishing. Otherwise, nothing will be played at the end.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** choosing another closing sound

   "sound_effects": [
     {
       "name": "closing_sound",
       "filename": "bye.ogg",
       "audio_channel_id": 2,
       "play_closing": false
     }
   ]

Change GPIO channels
====================

Change keymap
=============
.. TODO: check line numbers before publishing

If you want to change the default keymap used for the three push buttons, edit
the setting ``gpio_channels`` in the configuration file which can be opened with::

   $ start_dv -e cfg

.. literalinclude:: ../darth_vader_rpi/configs/default_main_cfg.json
   :language: python
   :lines: 8-26
   :emphasize-lines: 6, 12, 18
   :caption: **Default keymap used for the three push buttons**

In order to change the default keymap, you will need to change the value for
``key`` which is the name of the keyboard key associated with a given push
button.

The names of keyboard keys that you can use are those specified in the
`SimulRPi's documentation`_, e.g. `media_play_pause`, `shift`, and `shift_r`.

.. code-block:: python
   :emphasize-lines: 6
   :caption: **Example:** choosing ``shift_r`` for the *Quotes button*

    "gpio_channels": [
      {
        "channel_name": "quotes_button",
        "displa_name": "quotes_button",
        "channel_number": 25,
        "key": "shift_r"
      },
    ]

.. note::

   On mac, I recommend using the following keyboard keys because they don't
   require running the script ``start_dv`` with ``sudo``: *alt*, *alt_r*,
   *cmd*, *cmd_r*, *ctrl*, *ctrl_r*, *media_play_pause*,
   *media_volume_down*, *media_volume_mute*, *media_volume_up*, *shift*,
   and *shift_r*.

   **Ref.:** `Platform limitations`_

Change LED symbols
==================
By **default**, the symbols used for representing LEDs are the following:

   - 🛑 : LED turned ON
   - ⚪ : LED turned OFF

To change these default symbols, edit the setting ``gpio_channels`` by opening
the configuration file::

   $ start_dv -e cfg

As the name suggests, ``gpio_channels`` is a list of GPIO channels where each
item is an object defining a LED or a button and having the following
properties:

   - ``channel_name``: this property should **not be modified** because it is
     used to identify the correct GPIO channel when turning ON/OFF LEDs or
     checking a button's state.
   - ``display_name``: channel name that will be displayed in the terminal
     along with the LED symbol. By default, the channel number is displayed if
     ``display_name`` is not given.
   - ``channel_number``: based on the numbering system you have specified
     (`BOARD` or `BCM`).
   - ``led_symbols``: only defined for LED objects. It is a dictionary defining
     the symbols to be used when the LED is ON and OFF.

It is ``led_symbols`` that you need to modify in order to change the default
symbols for a given LED.

.. code-block:: bash
   :emphasize-lines: 7-8
   :caption: **Example:** changing the symbols for the lightsaber LED

    "gpio_channels": [
      {
         "channel_name": "lightsaber_led",
         "display_name": "lightsaber",
         "channel_number": 22,
         "led_symbols": {
           "ON": "\\033[1;31;48m(0)\\033[1;37;0m",
           "OFF": "(0)"️
         }
       }
    ]

.. note::

   If you omit ``led_symbols`` as a property for a LED object, the default LED
   symbols will be used instead.

Change paths to audio files
===========================
.. TODO: revisit this section once you are done with testing the installation of the package
.. TODO: check line number in URL to config file for sounds_directory

The setting ``sounds_directory`` in the `configuration file <https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L6>`__
defines the directory where all audio files (e.g. quotes) are saved.

The filename for each audio file is defined with respect to this directory
``sounds_directory``. Each audio object defined in the settings ``quotes``,
``songs`` and ``sound_effects`` have a ``filename`` property that you can
modify.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** filename for the *closing sound*

   "sound_effects": [
     {
       "name": "closing_sound",
       "filename": "quote_nooooo.ogg",
       "audio_channel_id": 2,
       "play_closing": false
     }
   ]

.. important::

   Don't change the ``name`` property for *songs* and *sound_effects* objects
   because it is used to identify the correct audio file to play when some
   event happens.

Change slot LEDs sequence
=========================

Mute breathing and closing sounds
=================================

Run script as quiet or verbose
==============================
