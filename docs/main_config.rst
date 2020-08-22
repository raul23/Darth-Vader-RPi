.. TODO: check line numbers in URLs
.. default_main_cfg
.. _audio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L55
.. _gpio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L8
.. _mode: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L5
.. _quiet: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L2
.. _quotes: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L73
.. _simulation: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L3
.. _slot_leds: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L49
.. _songs: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L111
.. _sound_effects: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L119
.. _sounds_directory: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L6
.. _verbose: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L4
.. external links
.. _logging configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_logging_cfg.json
.. _main configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json
.. _pygame: https://www.pygame.org/docs/
.. _pynput: https://pynput.readthedocs.io
.. _"I am your father": https://www.youtube.com/watch?v=xuJEYdOFEP4
.. _Imperial March song by Jacob Townsend: https://soundcloud.com/jacobtownsend1/imperial-march
.. _"Nooooo": https://www.youtube.com/watch?v=ZscVhFvD6iE
.. _RPi.GPIO: https://pypi.org/project/RPi.GPIO/
.. _RPIO.GPIO documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
.. _SimulRPi.GPIO: https://pypi.org/project/SimulRPi/
.. _Empire Strikes Back chest box light sequence: https://youtu.be/E2J_xl2MbGU?t=333
.. internal links
.. _default LED symbols: #default-led-symbols-label
.. _start_dv: README_docs.html#script-start-dv
.. _Add Darth Vader quotes: change_default_settings.html#add-darth-vader-quotes
.. _Change GPIO channel names and number: change_default_settings.html#change-gpio-channel-names-and-number
.. _Change keymap: change_default_settings.html#change-keymap-label
.. _Change LED symbols: change_default_settings.html#change-led-symbols-label

The main configuration file
===========================
The default settings used by the script ``start_dv`` are found in the
`main configuration file`_. It is referred to as *main* because there is another
config file you could edit, the `logging configuration file`_.

The *main* configuration file can be edited with the following command::

   $ start_dv -e cfg

The logging configuration file could be instead edited with the `-e log_cfg`
command-line option.

The previous command will open the configuration file with the default text
editor that is associated with JSON files as specified in your system, e.g.
*atom* on macOS or *vim* on Linux.

If you want to use another text editor you can specify it with the `-a APP`
command-line option::

   $ start_dv -e cfg -a TextEdit

In what follows, you wil find an explanation for each setting found in the
`main configuration file`_, presented in alphabetic order.

.. seealso::

    The script `start_dv`_

.. _audio-channels-label:

``audio_channels``
^^^^^^^^^^^^^^^^^^

Three audio channels are used for this project:

   - **channel 0**: used for the breathing sound which plays in the background
     almost as soon as the script ``start_dv`` runs. Its volume is set by
     default at 0.2 since we don't want to overwhelm the other sounds playing
     in the other channels
   - **channel 1**: used for playing the *Imperial March* song and all Darth
     Vader quotes.  Its volume is set by default at 1.0
   - **channel 2**: used for playing the lighsaber sound effects and the closing
     sound. Its volume is set by default at 1.0

The setting `audio_channels`_ in the configuration file defines these three
audio channels with their default volume.

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

The Python package `pygame`_ is used for playing the various sounds used in this
project.

.. note::

   - Volume takes values in the range 0.0 to 1.0 (inclusive).
   - If value < 0.0, the volume will not be changed
   - If value > 1.0, the volume will be set to 1.0

   As per the `pygame
   documentation <https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.set_volume>`__.

.. _gpio-channels-label:

``gpio_channels``
^^^^^^^^^^^^^^^^^
.. TODO: check line # in URL to ``gpio_channels``

The setting `gpio_channels`_ in the configuration file defines the GPIO pins
connected to LEDs and push buttons.

GPIO channels for the following I/O devices are defined:

   - **Lightsaber button**: controls the LEDs and sound effects for the
     lightsaber
   - **Song button**: when pressed it plays the *Imperial March* song
   - **Quotes button**: when pressed it plays one of Darth Vader quotes
   - **Slot LEDs**: consist of three LEDs referred to as *Top*, *Middle*, and
     *Top* LEDs and are found on Darth Vader's chest control box
   - **Lightsaber LED**: when the lightsaber button is pressed, this LED is
     turned ON/OFF

``gpio_channels`` lists GPIO channel objects with the following properties:

   - ``channel_name``: this property should **not be modified** because it is
     used to identify the correct GPIO channel when turning ON/OFF LEDs or
     checking a button's state
   - ``display_name``: channel name that will be displayed in the terminal
     along with the LED symbol. By default, the channel number is displayed if
     ``display_name`` is not given
   - ``channel_number``: identifies the GPIO pin based on the numbering system
     you have specified (`BOARD` or `BCM`)
   - ``key``: only defined for button objects. It specifies the mapping between
     a keyboard key and a push button so you can simulate push buttons with your
     keyboard

     .. code-block:: python
         :emphasize-lines: 5
         :caption: **Example:** changing keymap for the Song push button

          {
            "channel_name": "song_button",
            "display_name": "song_button",
            "channel_number": 24,
            "key": "shift_r"
          }

   - ``led_symbols``: only defined for LED objects. It is a dictionary defining
     the symbols to be used when the LED is turned ON and OFF. If nof found for
     a LED object, then the `default LED symbols`_ will be used

      .. code-block:: python
         :emphasize-lines: 5-7
         :caption: **Example:** changing the default LED symbols for the
                   lightsaber LED

          {
            "channel_name": "lightsaber_led",
            "display_name": "lightsaber",
            "channel_number": 22,
            "led_symbols": {
              "ON": "\\033[1;31;48m(0)\\033[1;37;0m",
              "OFF": "(0)"
            }
          }

.. _default-led-symbols-label:

By **default**, the symbols used for representing LEDs in the terminal are the
following:

   - 🛑 : LED turned ON
   - ⚪ : LED turned OFF

.. literalinclude:: ../darth_vader_rpi/configs/default_main_cfg.json
   :language: python
   :lines: 8-14, 42-47
   :caption: **Example:** GPIO channels for the lightsaber button and LED

Thus, in this example, you have a push button connected to the GPIO pin 23
(based on the BCM mode) and controlling the lightsaber by turning it ON/OFF
and producing the lightsaber sound effects (drawing, closing, and hum sounds).
Also, the keyboard key ``cmd`` simulates the lightsaber push button when
running the script ``start_dv`` on your computer.

Finally, the ligthsaber LED is connected to GPIO pin 22 (BCM) and is turned
ON/OFF when the corresponding push button (or ``cmd`` key) is pressed.

.. seealso::

   - `Change GPIO channel names and number`_
   - `Change keymap`_
   - `Change LED symbols`_

.. _mode-label:

``mode``
^^^^^^^^
The setting `mode`_ in the configuration file defines the numbering system
(`BOARD` or `BCM`) used to identify the GPIO channels. By default, `BCM` is
used.

As per the `RPIO.GPIO documentation`_:

   **BOARD** refers to the pin numbers on the P1 header of the Raspberry Pi
   board. The advantage of using this numbering system is that your hardware
   will always work, regardless of the board revision of the RPi. You will not
   need to rewire your connector or change your code.

   **BCM** is a lower level way of working - it refers to the channel numbers
   on the Broadcom SOC. You have to always work with a diagram of which channel
   number goes to which pin on the RPi board. Your script could break between
   revisions of Raspberry Pi boards.

.. _quiet-label:

``quiet``
^^^^^^^^^
The setting `quiet`_ in the configuration file is a flag (set to *false* by
default) that allows you to run the script ``start_dv`` without printing anything
on the terminal, not even the LED symbols when running the simulation nor the
exceptions are printed.

.. TODO: exceptions are displayed if happening before setting up logger in start_dv

.. code-block:: python
   :emphasize-lines: 2
   :caption: The setting ``quiet`` set to *false* by default

   {
     "quiet": false,
     "simulation": false,
     "verbose": false,
     "mode": "BCM"
   }

This flag can also be set directly through the script's command-line option
*-q*::

   $ start_dv -q

.. seealso::

   `Script's list of options <README_docs.html#list-of-options>`__

.. _quotes-label:

``quotes``
^^^^^^^^^^
The setting `quotes`_ in the configuration file defines all the Darth Vader's
quotes used for this project.

By default, two movie lines are included:

   - `"I am your father"`_
   - `"Nooooo"`_

.. TODO: check line in URL to config file showing ``quotes``

Each quote is represented in the configuration file as objects having the
following properties:

   - ``name``: it will be displayed in the terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: all quotes should be played in **channel 1** as
     explained in `audio_channels <#audio-channels-label>`__

.. code-block:: python
   :emphasize-lines: 3-5, 8-10
   :caption: **Example:** two Darth Vader quotes

    "quotes": [
      {
        "name": "dont_make_me_destroy_you",
        "filename": "quote_dont_make_me_destroy_you.ogg",
        "audio_channel_id": 1
      },
      {
        "name": "give_yourself_to_the_dark_side",
        "filename": "quote_give_yourself_to_the_dark_side.ogg",
        "audio_channel_id": 1
      }
    ]

.. important::

   All Darth Vader quotes should be played in **channel 1** as explained in
   `audio_channels <#audio-channels-label>`__

.. seealso::

   `Add Darth Vader quotes`_

.. _simulation-label:

``simulation``
^^^^^^^^^^^^^^
The setting `simulation`_ in the configuration file is a flag (set to *false* by
default) that allows you to run the script ``start_dv`` on your computer,
instead of a Raspberry Pi (RPi).

The module `SimulRPi.GPIO`_ is used in order to partly fake `RPi.GPIO`_ and
simulate I/O devices connected to an RPi such as LEDs and push buttons by
displaying LED symbols in the terminal and monitoring the keyboard for any
pressed key.

This flag can also be set directly through the script's command-line option
*-s*::

   $ start_dv -s

.. note::

   `SimulRPi.GPIO`_ makes use of the package `pynput`_ to monitor the keyboard
   for any pressed key.

.. seealso::

   `Script's list of options <README_docs.html#list-of-options>`__

.. _slot-leds-label:

``slot_leds``
^^^^^^^^^^^^^
Three LEDs (labeled as *bottom*, *middle*, and *top*) illuminate the slots in
Darth Vader's chest control box.

The setting `slot_leds`_ in the configuration file defines the sequence the
slot LEDs should be turned ON/OFF. This sequence corresponds to Darth Vader's
physiological state, e.g. if he is in a calm mood the slot LEDs will blink in a
different pattern than if he was angry.

``slot_leds`` is an object that takes the following properties:

   - ``delay_subsequences``: delay in seconds between subsequences of LEDs, i.e.
     between each step in the sequence
   - ``time_leds_on``: time in seconds the LEDs will be turned on
   - ``sequence``: the name of the sequence which can be either *"action"*
     or *"calm"* or a `custom sequence <#custom-sequence-label>`__

.. code-block:: python
   :caption: **Example:** a slot_leds object with the action sequence

      "slot_leds":{
        "delay_subsequences": 0.5,
        "time_leds_on": 1,
        "sequence": "action"
      },

.. _custom-sequence-label:

The user can also provide its own sequence by using a list of LED labels
{'top', 'midddle', 'bottom'} arranged in a sequence as to specify the order the
slot LEDs should turn ON/OFF.

**Example:** custom slot LEDs sequence

.. code-block:: python

   "sequence":[
     ["top", "bottom"],
     [],
     ["middle"],
     []
   ]

This simple sequence will turn ON/OFF the slot LEDs in this order::

  1. top + bottom LEDs turned ON
  2. All LEDs turned OFF
  3. middle LED turned ON
  4. All LEDs turned OFF

.. note::

   This is how the *action* and *calm* sequences are exactly defined:

   .. code-block:: python
      :caption: **Action sequence**

      "sequence":[
        ["top", "middle", "bottom"],
        ["top", "bottom"],
        ["top", "middle", "bottom"],
        ["top"],
        [],
        ["top", "middle", "bottom"],
        ["top"],
        ["top", "middle", "bottom"],
        ["middle", "bottom"],
        [],
        ["top", "bottom"],
        ["top", "middle", "bottom"],
        ["top", "bottom"],
        [],
        ["top"],
        []
      ]

   .. code-block:: python
      :caption: **Calm sequence**

      "sequence":[
        ["middle"],
        ["top"],
        ["middle"],
        ["top"],
        ["middle"],
        ["top"],
        ["top"],
        [],
        ["bottom"],
        []
      ]

.. note::

   The default sequences of slot LEDs were obtained from
   `Empire Strikes Back chest box light sequence`_.

.. _songs-label:

``songs``
^^^^^^^^^
The setting `songs`_ in the configuration file defines the songs that can be
played as part of the project.

At the moment, only the `Imperial March song by Jacob Townsend`_ is supported.

The setting ``songs`` takes a list of song objects having the following
properties:

   - ``name``: the name of the song which will be shown in the terminal
   - ``filename``: is relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: all songs should be played in **channel 1** as
     explained in `audio_channels <#audio-channels-label>`__

.. important::

   All songs should be played in **channel 1** as explained in
   `audio_channels <#audio-channels-label>`__

.. _sound-effects-label:

``sound_effects``
^^^^^^^^^^^^^^^^^
The setting `sound_effects`_ in the configuration file defines the following
sounds:

   - **Breathing sound**: almost as soon as the script ``start_dv`` runs, Darth
     Vader's breathing sound starts playing in the background until the script
     ends
   - **Lightsaber drawing sound**: when the lightsaber button is pressed, the
     drawing sound is played first followed by the hum sound until the button is
     pressed again which will produce the retraction sound
   - **Lightsaber hum sound**: plays immediately after the lightsaber drawing
     sound until the lightsaber button is pressed again
   - **Lightsaber retraction sound**: plays when the lightsaber button is
     pressed while the hum sound is playing
   - **Closing sound**: plays after the user presses ``ctrl`` + ``c`` to exit
     from the script. By default, it is not played at the end

``sound_effects`` takes a list of sound objects having the following properties:

   - ``name``: name of the sound which will be displayed in the terminal
   - ``filename``: relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: the audio channel used for playing the sound. See
     `audio_channels <#audio-channels-label>`__ to know what channel is used for
     each type of sounds
   - ``play_opening``: if set to *true*, the sound will be played at the start of
     the script
   - ``loops``: number of times the sound should be repeated. If set to -1, it
     will be repeated indefinitely
   - ``play_closing``: only defined for the *closing_sound* object. If set to
     *true*, the sound will play at the end of the script.

.. code-block:: python
   :emphasize-lines: 3, 10
   :caption: **Example:** two sound effects

      "sound_effects": [
        {
          "name": "breathing_sound",
          "filename": "darth_vader_breathing.ogg",
          "audio_channel_id": 0,
          "play_opening": true,
          "loops": -1
        },
        {
          "name": "closing_sound",
          "filename": "quote_nooooo.ogg",
          "audio_channel_id": 2,
          "play_closing": false
        }
      ]

.. _sounds_directory-label:

``sounds_directory``
^^^^^^^^^^^^^^^^^^^^
The setting `sounds_directory`_ in the configuration file defines the directory
where all the audio files are saved.

All the audio filenames found in the configuration file are defined relative to
``sounds_directory``.

.. code-block:: python
   :emphasize-lines: 4
   :caption: **Example:** Filename for the breathing-sound audio file

   "sound_effects": [
     {
       "name": "breathing_sound",
        "filename": "darth_vader_breathing.ogg",
        "audio_channel_id": 0,
        "play_opening": true,
        "loops": -1
     }
   ]

In this example, the audio file `darth_vader_breathing.ogg` is to be found in
the directory ``sounds_directory``.

.. _verbose-label:

``verbose``
^^^^^^^^^^^
The setting `verbose`_ in the configuration file is a flag (set to *false* by
default) that allows you to run the script ``start_dv`` by logging to the
terminal any message with at least a DEBUG level. Also, when there is an
exception, a traceback is printed so you can pinpoint exactly where the error
occurred in the code which is not the case when running the script without
``verbose`` (you only get the error message).

.. code-block:: console
   :caption: **Example:** running the script **without verbose**

   ERROR    AttributeError: 'Namespace' object has no attribute 'edits'
   ERROR    Program exited with 1

.. code-block:: console
   :caption: **Example:** running the script **with verbose**

   ERROR    'Namespace' object has no attribute 'edits'
   Traceback (most recent call last):
     File "start_dv.py", line 795, in main
       if args.edits:
   AttributeError: 'Namespace' object has no attribute 'edits'
   ERROR    Program exited with 1

This flag can also be set directly through the script's command-line option
*-v*::

   $ start_dv -v

.. seealso::

   `Script's list of options <README_docs.html#list-of-options>`__
