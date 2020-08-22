.. TODO: check line numbers in URLs
.. default_main_cfg
.. _audio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L55
.. _closing_sound: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L143
.. _configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L1
.. _gpio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L8
.. _quotes: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L73
.. _sound_effects: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L119
.. _sounds_directory: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L6
.. external links
.. _logging configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_logging_cfg.json
.. _"Nooooo": https://www.youtube.com/watch?v=ZscVhFvD6iE
.. internal links
.. _default symbols: main_config.html#default-led-symbols-label
.. _start_dv: README_docs.html#script-start-dv
.. _The main configuration file: main_config.html

=======================
Change default settings
=======================

.. contents::
   :depth: 2
   :local:

Important tips
==============
- This is the command to edit the configuration file with the **default** text
  editor::

   $ start_dv -e cfg

  Or with a **specific** text editor::

   $ start_dv -e cfg -a APP_NAME

- To end the script ``start_dv``, press ``ctrl`` + ``c``
- When adding audio files, don't use *mp3* as the file format. Instead, use
  *ogg* (compressed) or *wav* (uncompressed). The reason is that *mp3* won't
  work well with pygame's simultaneous playback capability.

  **Reference:** `stackoverflow <https://stackoverflow.com/a/59742418>`__

.. seealso::

     The script `start_dv`_

.. _add-darth-vader-quotes-label:

Add Darth Vader quotes
======================
If you want to add more Darth Vader quotes, you have to edit the setting
`quotes`_ in the configuration file. Open the configuration file with::

   $ start_dv -e cfg

Each quote is represented in the configuration file as objects having the
following properties:

   - ``name``: it will be displayed in the terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <main_config.html#sounds-directory-label>`__
   - ``audio_channel_id``: all quotes should be played in **channel 1** as
     explained in `audio_channels <main_config.html#audio-channels-label>`__

Add your quote object to the list in ``quotes``, like in the following example:

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

.. seealso::

   The setting `quotes <main_config.html#quotes-label>`__

.. _change-channel-volume-label:

Change channel volume
=====================
To change the volume for an audio channel, open the configuration file and edit
the channel's volume found in the setting `audio_channels`_::

   $ start_dv -e cfg

.. code-block:: python
   :emphasize-lines: 5, 10, 15
   :caption: **Audio channels and their default volume**

   "audio_channels": [
     {
       "name": "breathing_sound",
       "audio_channel_id": 0,
       "volume": 0.2
     },
     {
       "name": "song_and_quotes",
       "audio_channel_id": 1,
       "volume": 1.0
     },
     {
       "name": "lightsaber_and_closing_sounds",
       "audio_channel_id": 2,
       "volume": 1.0
     }
   ],

What each channel controls:

   - **Channel 0** controls Darth Vader's breathing sound
   - **Channel 1** controls the *Imperial March song* and all Darth Vader quotes
   - **Channel 2** controls the lighsaber sound effects and the closing sound

.. note::

   Volume takes values in the range 0.0 to 1.0 (inclusive). As per the `pygame
   documentation <https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.set_volume>`__.

.. seealso::

   The setting `audio_channels <main_config.html#audio-channels-label>`__

.. _change-closing-sound-label:

Change closing sound
====================
When the script is exiting after the user presses ``ctrl`` + ``c``, a sound is
produced which by default is the `"Nooooo"`_ quote.

To change the default closing sound, edit the setting `sound_effects`_ in the
configuration file which can be opened with::

   $ start_dv -e cfg

At the end of the list in ``sound_effects``, you will find the `closing_sound`_
object. These are the properties you can modify for this object:

   - ``filename``: relative to
     `sounds_directory <main_config.html#sounds-directory-label>`__
   - ``play_closing``: if *true*, the closing sound will be played when the
     script is finishing. Otherwise, nothing will be played at the end.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** choosing another closing sound by changing ``filename``

   "sound_effects": [
     {
       "name": "closing_sound",
       "filename": "bye.ogg",
       "audio_channel_id": 2,
       "play_closing": false
     }
   ]

.. seealso::

   - `Mute breathing and closing sounds <#mute-breathing-and-closing-sounds-label>`__
   - The setting `sound_effects <main_config.html#sound-effects-label>`__

.. _change-gpio-channel-names-and-numer-label:

Change GPIO channel names and number
====================================

.. _change-keymap-label:

Change keymap
=============
.. TODO: check line numbers before publishing

If you want to change the default keymap used for the three push buttons, edit
the setting `gpio_channels`_ in the configuration file which can be opened with::

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
:simulapi:`SimulRPi's documentation <content-default-keymap-label>`, e.g.
`media_play_pause`, `shift`, and `shift_r`.

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

   **Ref.:** :simulapi:`Platform limitations <important-platform-limitations-label>`

.. seealso::

   The setting `gpio_channels <main_config.html#gpio-channels-label>`__

.. _change-led-symbols-label:

Change LED symbols
==================
To change the `default symbols`_ used for representing LEDs in the terminal,
edit the setting `gpio_channels`_ by opening the configuration file::

   $ start_dv -e cfg

You need to modify the property ``led_symbols`` for a given LED object defined
in ``gpio_channels``.

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

   If you omit ``led_symbols`` as a property for a LED object, the
   `default symbols`_ will be used instead.

.. seealso::

   - `Change slot LEDs sequence <#change-slot-leds-sequence-label>`__
   - The setting `gpio_channels <main_config.html#gpio-channels-label>`__

Change paths to audio files
===========================
.. TODO: revisit this section once you are done with testing the installation of the package
.. TODO: check line number in URL to config file for sounds_directory

The setting `sounds_directory`_ in the configuration file defines the directory
where all audio files (e.g. quotes) are saved.

The filename for each audio file is defined with respect to the directory
`sounds_directory <main_config.html#sounds-directory-label>`__. Each audio
object defined in the settings ``quotes``, ``songs`` and ``sound_effects`` have
a ``filename`` property that you can modify.

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

.. seealso::

   The setting `sound_effects <main_config.html#sound-effects-label>`__

.. _change-slot-leds-sequence-label:

Change slot LEDs sequence
=========================

.. _mute-breathing-and-closing-sounds-label:

Mute breathing and closing sounds
=================================

.. _run-script-as-quiet-or-verbose-label:

Run script as quiet or verbose
==============================
