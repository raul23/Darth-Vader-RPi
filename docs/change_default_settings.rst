===========================
Change the default settings
===========================

.. contents::
   :depth: 2
   :local:

Important tips
==============
- This is the command to edit the `configuration file`_ with a **default**
  text editor as defined in your system::

   $ start_dv -e cfg

  Or with a **specific** text editor::

   $ start_dv -e cfg -a APP_NAME

  where *APP_NAME* is the name of a text editor, e.g. TextEditor

- To end the script :mod:`start_dv`, press ``ctrl`` + ``c``
- When adding audio files, don't use *mp3* as the file format. Instead, use
  *ogg* (compressed) or *wav* (uncompressed). The reason is that *mp3* won't
  work well with pygame's simultaneous playback capability.

  **Reference:** `stackoverflow <https://stackoverflow.com/a/59742418>`__

.. _add-darth-vader-quotes-label:

Add Darth Vader quotes
======================
If you want to add more Darth Vader quotes, you have to edit the setting
`quotes`_ in the configuration file. Open the configuration file with::

   $ start_dv -e cfg

Each quote is represented in the configuration file as objects having the
following properties:

   - ``id``: unique identifier
   - ``name``: it will be displayed in the terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <main_config.html#sounds-directory-label>`__
   - ``audio_channel_id``: all quotes should be played in **channel 1** as
     explained in `audio_channels <main_config.html#audio-channels-label>`__

Add your quote object to the list in ``quotes``, like in the following example:

.. code-block:: python
   :emphasize-lines: 3-6
   :caption: **Example:** adding a new quote

   "quotes": [
     {
       "id": "there_is_no_escape",
       "name": "There is no escape",
       "filename": "quote_there_is_no_escape.ogg",
       "audio_channel_id": 1
     },

.. seealso::

   - The setting `audio_channels <main_config.html#audio-channels-label>`__
   - The setting `quotes <main_config.html#quotes-label>`__
   - `Change channel volume <#change-channel-volume-label>`__
   - `Change paths to audio files <#change-paths-to-audio-files-label>`__

.. _change-channel-volume-label:

Change channel volume
=====================
To change the volume for an audio channel, open the configuration file and edit
the channel's ``volume`` found in the setting `audio_channels`_::

   $ start_dv -e cfg

.. code-block:: python
   :emphasize-lines: 5, 10, 15
   :caption: **Audio channels and their default volume**

   "audio_channels": [
     {
       "channel_id": 0,
       "channel_name": "breathing_sound",
       "volume": 0.2
     },
     {
       "channel_id": 1,
       "name": "song_and_quotes",
       "volume": 1.0
     },
     {
       "channel_id": 2,
       "name": "lightsaber_and_closing_sounds",
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
When the script :mod:`start_dv` is exiting after the user presses
``ctrl`` + ``c``, a sound is produced. By default, no closing sound is produced
and if it were to play, it would be the `"Nooooo"`_ quote.

To change the default closing sound, edit the setting `sound_effects`_ in the
configuration file which can be opened with::

   $ start_dv -e cfg

At the end of the list in ``sound_effects``, you will find the `closing_sound`_
object. These are the properties you can modify for this object:

   - ``name``: it is the name of the sound which will be displayed in the
     terminal
   - ``filename``: it is relative to
     `sounds_directory <main_config.html#sounds-directory-label>`__
   - ``mute``: if *true*, nothing will be played at the end of the script.
     Otherwise, the closing sound will be played when the script is terminating.

.. code-block:: python
   :emphasize-lines: 5
   :caption: **Example:** choosing another closing sound by changing ``filename``

   "sound_effects": [
     {
       "id": "closing_sound",
       "name": "Bye [Closing]",
       "filename": "bye.ogg",
       "audio_channel_id": 2,
       "mute": false
     },

.. note::

   By default, the closing sound is not played at the end of the script
   :mod:`start_dv`. Set its property ``mute`` to *true* in order to play the
   closing sound when the script exits.

.. seealso::

   - The setting `audio_channels <main_config.html#audio-channels-label>`__
   - The setting `sound_effects <main_config.html#sound-effects-label>`__
   - `Change channel volume <#change-channel-volume-label>`__
   - `Change paths to audio files <#change-paths-to-audio-files-label>`__

.. _change-gpio-channel-name-and-number-label:

Change GPIO channel name and number
===================================
The `GPIO channels`_ are identified in the terminal by their ``channel_name``
along with their LED symbols. If ``channel_name`` is not available, then its
``channel_number`` is shown.

The ``channel_number`` is the GPIO channel number of a pin used for connecting
an I/O device (e.g. LED) and is defined based on the numbering system you have
specified (*BOARD* or *BCM*).

To change a GPIO channel's ``channel_name`` and ``channel_number``, open the
configuration file with::

   $ start_dv -e cfg

And edit its properties ``channel_name`` and ``channel_number``, like in the
following example.

.. code-block:: python
   :emphasize-lines: 4-5
   :caption: **Example:** changing the ``channel_name`` and ``channel_number``
             for the bottom LED

   "gpio_channels": [
     {
       "channel_id": "bottom_led",
       "channel_name": "Bottom LED",
       "channel_number": 15
     },

.. important::

   Don't change the property ``channel_id`` since it is used to uniquely
   identify the GPIO channels.

.. seealso::

   The setting `gpio_channels <main_config.html#gpio-channels-label>`__

.. _change-keymap-label:

Change keymap
=============
.. TODO: check line numbers before publishing

If you want to change the default keymap used for the three push buttons, edit
the setting `gpio_channels`_ in the configuration file which can be opened with::

   $ start_dv -e cfg

.. code-block:: python
   :emphasize-lines: 6, 12, 18
   :caption: **Default keymap used for the three push buttons**

   "gpio_channels": [
     {
       "channel_id": "lightsaber_button",
       "channel_name": "lightsaber_button",
       "channel_number": 23,
       "key": "cmd"
     },
     {
       "channel_id": "song_button",
       "channel_name": "song_button",
       "channel_number": 24,
       "key": "alt"
     },
     {
       "channel_id": "quotes_button",
       "channel_name": "quotes_button",
       "channel_number": 25,
       "key": "alt_r"
     },

In order to change the default keymap, you will need to change the value for
``key`` which refers to the name of the keyboard key associated with a given
push button.

The names of keyboard keys that you can use are those specified in the
:simulapi:`SimulRPi's documentation <content-default-keymap-label>`, e.g.
`media_play_pause`, `shift`, and `shift_r`.

.. code-block:: python
   :emphasize-lines: 5
   :caption: **Example:** choosing ``shift_r`` for the *Quotes button*

   {
     "channel_id": "quotes_button",
     "channel_name": "quotes_button",
     "channel_number": 25,
     "key": "shift_r"
   },

.. note::

   On mac, I recommend using the following keyboard keys because they don't
   require running the script :mod:`start_dv` with ``sudo``: *alt*, *alt_r*,
   *cmd*, *cmd_r*, *ctrl*, *ctrl_r*, *media_play_pause*,
   *media_volume_down*, *media_volume_mute*, *media_volume_up*, *shift*,
   and *shift_r*.

   **Ref.:** :simulapi:`Platform limitations <important-platform-limitations-label>`

.. seealso::

   The setting `gpio_channels <main_config.html#gpio-channels-label>`__

.. _change-led-symbols-label:

Change LED symbols
==================
You can either:

   1. change the default LED symbols used by **all** output channels, or
   2. change the LED symbols for **specific** output channels

Case 1: change ``default_led_symbols``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To change the `default LED symbols`_ used by **all** output channels, edit the
setting `default_led_symbols`_ by opening the configuration file::

   $ start_dv -e cfg

Add your LED symbols for each output state::

   "default_led_symbols": {
     "ON": "🔵",
     "OFF": "⚪ "
   },

Case 2: change ``gpio_channels``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To change the LED symbols for **specific** output channels, edit the setting
`gpio_channels`_ by opening the configuration file::

   $ start_dv -e cfg

You need to modify the property ``led_symbols`` for a given LED object defined
in ``gpio_channels``.

.. code-block:: bash
   :emphasize-lines: 7-8
   :caption: **Example:** changing the symbols for the lightsaber LED

    "gpio_channels": [
      {
         "channel_id": "lightsaber_led",
         "channel_name": "lightsaber",
         "channel_number": 22,
         "led_symbols": {
           "ON": "\\033[1;31;48m(0)\\033[1;37;0m",
           "OFF": "(0)"️
         }
       }
    ]

.. note::

   If you omit ``led_symbols`` as a property for a LED object, the
   `default LED symbols`_ will be used instead.

.. important::

   If you are having problems displaying the default LED symbols when running
   the script :mod:`start_dv`, such as this error:

   .. code-block:: console

      ERROR    UnicodeEncodeError: 'ascii' codec can't encode character '\U0001f6d1' in position 2: ordinal not in range(128)

   Then, you are might have your locale settings set incorrectly. Check
   `Display problems`_ for more info about how to change them properly or
   other solutions.

.. seealso::

   - The setting `gpio_channels <main_config.html#gpio-channels-label>`__
   - `Change slot LEDs sequence <#change-slot-leds-sequence-label>`__

.. _change-paths-to-audio-files-label:

Change paths to audio files
===========================
.. TODO: revisit this section once you are done with testing the installation of the package
.. TODO: check line number in URL to config file for sounds_directory

The setting `sounds_directory`_ in the configuration file defines the directory
where all audio files (e.g. quotes) are saved.

Each audio object defined in the settings ``quotes``, ``songs`` and
``sound_effects`` have a ``filename`` property that you can modify. The
filename for each audio file is defined with respect to the directory
`sounds_directory <main_config.html#sounds-directory-label>`__.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** filename for the *closing sound*

   "sound_effects": [
     {
       "id": "closing_sound",
       "filename": "quote_nooooo.ogg",
       "audio_channel_id": 2,
       "mute": false
     },

.. important::

   Don't change the ``id`` property for *songs* and *sound_effects* objects
   because it is used to uniquely identify them.

.. seealso::

   - The setting `quotes <main_config.html#quotes-label>`__
   - The setting `songs <main_config.html#songs-label>`__
   - The setting `sound_effects <main_config.html#sound-effects-label>`__
   - The setting `sounds_directory <main_config.html#sounds-directory-label>`__

.. _change-slot-leds-sequence-label:

Change slot LEDs sequence
=========================
The setting `slot_leds`_ in the configuration file control the blinking
pattern of the three slot LEDs in Darth Vader's control box.

To change the default sequence, open the configuration file::

   $ start_dv -e cfg

The ``slot_leds`` object defines the property ``sequence`` which can take a
string value ('*action*' or '*calm*') or a custom sequence.

The custom sequence consists of a list of LED labels {*'top'*, *'middle'*,
*'bottom'*} arranged in a sequence specifying the order the slot LEDs should
turn ON/OFF.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** a ``slot_leds`` object with the **calm** sequence

      "slot_leds":{
        "delay_between_steps": 0.5,
        "time_per_step": 1,
        "sequence": "calm"
      },

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** a ``slot_leds`` object with a **custom** sequence

      "slot_leds":{
        "delay_between_steps": 0.5,
        "time_per_step": 1,
        "sequence":[
          ["top", "bottom"],
          [],
          ["middle"],
          []
        ]
      },

This simple custom sequence will turn ON/OFF the slot LEDs in this order::

  1. top + bottom LEDs turned ON
  2. All LEDs turned OFF
  3. middle LED turned ON
  4. All LEDs turned OFF

Each step in the sequence will lasts for ``time_per_step`` seconds and there will
be a delay of ``delay_between_steps`` seconds between each step in the sequence.
And the whole sequence will keep on repeating until the script exits by
pressing ``ctrl`` + ``c``.

.. seealso::

   The setting `slot_leds <main_config.html#slot-leds-label>`__

.. _mute-breathing-sound-label:

Mute breathing sound
====================
To mute Darth Vader's breathing sound which plays almost as soon as the
script :mod:`start_dv` runs, edit the setting `sound_effects`_ in the
configuration file which can be opened with::

   $ start_dv -e cfg

Set the *breathing_sound* object's ``mute`` to *false*.

.. code-block:: python
   :emphasize-lines: 7
   :caption: **Example:** Mute the breathing sound

      "sound_effects": [
        {
          "id": "breathing_sound",
          "name": "Breathing sound",
          "filename": "darth_vader_breathing.ogg",
          "audio_channel_id": 0,
          "mute": false,
          "loops": -1
        }
      ]

.. seealso::

   - The setting `sound_effects <main_config.html#sound-effects-label>`__
   - `Change channel volume <#change-channel-volume-label>`__

.. _run-script-as-quiet-or-verbose-label:

Run script as quiet or verbose
==============================
To run the script :mod:`start_dv` as quiet or verbose, open the configuration
file with::

   $ start_dv -e cfg

And set the setting `quiet`_ or `verbose`_ to *true*.

When running the script :mod:`start_dv` as ``verbose``, the logging level is
set to *DEBUG*. Thus, all messages will be displayed and when there is an
exception, the traceback will be shown.

On the other hand, when running the script :mod:`start_dv` as ``quiet``,
nothing will be printed to the terminal, not even error messages. However, you
will still be able to hear sounds and interact with the push buttons or
keyboard.

.. important::

   if ``quiet`` and ``verbose`` are both activated at the same time, only
   ``quiet`` will have an effect.

.. seealso::

   - The setting `quiet <main_config.html#quiet-label>`__
   - The setting `verbose <main_config.html#verbose-label>`__
