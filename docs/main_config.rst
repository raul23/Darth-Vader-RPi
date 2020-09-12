The main configuration file
===========================
The default settings used by the script :mod:`start_dv` are found in the
`main configuration file`_. It is referred to as *main* because there is
another config file you could edit, the `logging configuration file`_.

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

.. important::

   Some of the settings (`quiet <#quiet-label>`__,
   `simulation <#simulation-label>`__, and `verbose <#verbose-label>`__) in
   the configuration file can be also set through the script's command-line
   arguments. The command-line arguments override the settings found in the
   configuration file.

.. seealso::

    The script `start_dv`_

.. _audio-channels-label:

``audio_channels``
^^^^^^^^^^^^^^^^^^

Three audio channels are used for this project:

   - **channel 0**: used for Darth Vader's breathing sound which plays in the
     background almost as soon as the script :mod:`start_dv` runs. Its volume
     is set by default at 0.2 since we don't want to overwhelm the other sounds
     playing in the other audio channels
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
       "channel_id": 0,
       "channel_name": "breathing_sound",
       "volume": 0.2
     },
     {
       "channel_id": 1,
       "channel_name": "song_and_quotes",
       "volume": 1.0
     },
     {
       "channel_id": 2,
       "channel_name": "lightsaber_and_closing_sounds",
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

.. _default-led-symbols-label:

``default_led_symbols``
^^^^^^^^^^^^^^^^^^^^^^^
The setting `default_led_symbols`_ in the configuration file defines the
default LED symbols used by **all** output channels. A LED symbol is used for
each output state (*ON* and *OFF*).

By **default**, the symbols used for representing LEDs in the terminal are the
following::

   "default_led_symbols": {
     "ON": "🛑",
     "OFF": "⚪"
   },

.. seealso::

   `Change LED symbols`_

.. _gpio-channels-label:

``gpio_channels``
^^^^^^^^^^^^^^^^^
.. TODO: check line # in URL to ``gpio_channels``

The setting `gpio_channels`_ in the configuration file defines the GPIO pins
connected to LEDs and push buttons.

GPIO channels for the following I/O devices are defined:

   - **Lightsaber button**: it controls the LEDs and sound effects for the
     lightsaber
   - **Song button**: when pressed it plays the *Imperial March* song
   - **Quotes button**: when pressed it plays one of Darth Vader quotes
   - **Slot LEDs**: they consist of three LEDs referred to as *Top*, *Middle*,
     and *Bottom* LEDs and are found on Darth Vader's chest control box
   - **Lightsaber LEDs**: when the lightsaber button is pressed, these LEDs are
     turned ON/OFF

``gpio_channels`` lists GPIO channel objects with the following properties:

   - ``channel_id``: this property should **not be modified** because it is
     used to uniquely identify the GPIO channels
   - ``channel_name``: it will be displayed in the terminal along with the LED
     symbol. By default, the channel number is displayed if ``channel_name`` is
     the empty string, i.e. ``channel_name = ""``
   - ``channel_number``: it identifies the GPIO pin based on the numbering
     system you have specified (`BOARD` or `BCM`)
   - ``key``: it is only defined for button objects. It specifies the mapping
     between a keyboard key and a push button so you can simulate push buttons
     with your keyboard

     .. code-block:: python
         :emphasize-lines: 5
         :caption: **Example:** changing keymap for the Song button

          {
            "channel_id": "song_button",
            "channel_name": "song_button",
            "channel_number": 24,
            "key": "shift_r"
          }

   - ``led_symbols``: it is only defined for LED objects. It is a dictionary
     defining the symbols to be used when the LED is turned ON and OFF. If not
     found for a LED object, then the `default LED symbols`_ will be used

      .. code-block:: python
         :emphasize-lines: 5-8
         :caption: **Example:** changing the default LED symbols for the
                   lightsaber LED

          {
            "channel_id": "lightsaber_led",
            "channel_name": "lightsaber",
            "channel_number": 22,
            "led_symbols": {
              "ON": "\\033[1;31;48m(0)\\033[1;37;0m",
              "OFF": "(0)"
            }
          }

Let's take a look at two GPIO channels found in the configuration file:

.. code-block:: python
   :caption: **Example:** GPIO channels for the lightsaber button and LEDs

   "gpio_channels": [
     {
       "channel_id": "lightsaber_button",
       "channel_name": "lightsaber_button",
       "channel_number": 23,
       "key": "cmd"
     },
     {
       "channel_id": "lightsaber_led",
       "channel_name": "lightsaber",
       "channel_number": 22
     }
   ]

Thus, in this example, you have a push button connected to the GPIO pin 23
(based on the BCM mode), controlling the lightsaber by turning it ON/OFF and
producing the lightsaber sound effects (drawing, retraction, and hum sounds).
Also, the keyboard key ``cmd`` simulates the lightsaber push button when
running the script :mod:`start_dv` on your computer.

Finally, the ligthsaber LEDs are connected to GPIO pin 22 (BCM) and are turned
ON/OFF when the corresponding push button (or ``cmd`` key) is pressed.

.. seealso::

   - `Change GPIO channel name and number`_
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
default) that allows you to run the script :mod:`start_dv` without printing
anything on the terminal, not even the LED symbols when running the simulation
nor the exceptions are printed.

However, you will still be able to hear sounds and interact with the push
buttons or keyboard.

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

   `Script's list of options`_

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

   - ``id``: unique identifier
   - ``name``: it will be displayed in the terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: all quotes should be played in **channel 1** as
     explained in `audio_channels <#audio-channels-label>`__

.. code-block:: python
   :emphasize-lines: 3-6, 9-12
   :caption: **Example:** two Darth Vader quotes

    "quotes": [
      {
        "id": "dont_make_me_destroy_you",
        "name": "Don't make me destroy you",
        "filename": "quote_dont_make_me_destroy_you.ogg",
        "audio_channel_id": 1
      },
      {
        "id": "give_yourself_to_the_dark_side",
        "name": "Give yourself to the dark side",
        "filename": "quote_give_yourself_to_the_dark_side.ogg",
        "audio_channel_id": 1
      }
    ]

.. important::

   All Darth Vader quotes should be played in **channel 1** as explained in
   `audio_channels <#audio-channels-label>`__

.. seealso::

   - The setting `audio_channels <#audio-channels-label>`__
   - `Add Darth Vader quotes`_
   - `Change channel volume <change_default_settings.html#change-channel-volume-label>`__
   - `Change paths to audio files <change_default_settings.html#change-paths-to-audio-files-label>`__

.. _simulation-label:

``simulation``
^^^^^^^^^^^^^^
The setting `simulation`_ in the configuration file is a flag (set to *false* by
default) that allows you to run the script :mod:`start_dv` on your computer,
instead of a Raspberry Pi (RPi).

The module `SimulRPi.GPIO`_ is used in order to partly fake `RPi.GPIO`_ and
simulate I/O devices connected to an RPi such as LEDs and push buttons by
displaying LED symbols in the terminal and monitoring the keyboard for any
pressed key.

This flag can also be set directly through the script's command-line option
*-s*::

   $ start_dv -s

.. note::

   :mod:`SimulRPi.GPIO` makes use of the package `pynput`_ to monitor the keyboard
   for any pressed key.

.. seealso::

   `Script's list of options`_

.. _slot-leds-label:

``slot_leds``
^^^^^^^^^^^^^
Three LEDs (labeled as *top*, *middle*, and *top*) illuminate the slots in
Darth Vader's chest control box.

The setting `slot_leds`_ in the configuration file defines the sequence the
slot LEDs should be turned ON/OFF. This sequence corresponds to Darth Vader's
physiological state, e.g. if he is in a calm mood the slot LEDs will blink in a
different pattern than if he was in action.

``slot_leds`` is an object that takes the following properties:

   - ``delay_between_steps``: delay in seconds between each step in the sequence
   - ``time_per_step``: time in seconds each step will last
   - ``sequence``: the type of the sequence which can be either *"action"*,
     *"calm"* or a `custom sequence <#custom-sequence-label>`__. The sequence
     will keep on repeating until the script exits

.. code-block:: python
   :caption: **Example:** a ``slot_leds`` object with the calm sequence

      "slot_leds":{
        "delay_between_steps": 0.5,
        "time_per_step": 1,
        "sequence": "calm"
      },

.. _custom-sequence-label:

The user can also provide its own sequence by using a list of LED labels
{*'top'*, *'middle'*, *'bottom'*} arranged in a sequence specifying the
order the slot LEDs should turn ON/OFF.

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

Each step in the sequence will lasts for ``time_per_step`` seconds and there will
be a delay of ``delay_between_steps`` seconds between each step in the sequence.
And the whole sequence will keep on repeating until the script exits.

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

   The default sequences of slot LEDs were obtained from this YouTube video:
   `Empire Strikes Back chest box light sequence`_.

.. seealso::

   `Change slot LEDs sequence <change_default_settings.html#change-slot-leds-sequence-label>`__

.. _songs-label:

``songs``
^^^^^^^^^
The setting `songs`_ in the configuration file defines the songs that can be
played as part of the project.

At the moment, only the `Imperial March song by Jacob Townsend`_ is supported.

The setting ``songs`` takes a list of song objects having the following
properties:

   - ``id``: this property should **not be modified** because it is
     used to uniquely identify the songs
   - ``name``: the name of the song which will be shown in the terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: all songs should be played in **channel 1** as
     explained in `audio_channels <#audio-channels-label>`__

.. code-block:: python
   :emphasize-lines: 4, 6
   :caption: The **Imperial March** song playing in audio channel #1

      "songs": [
        {
          "id": "imperial_march_song",
          "name": "Imperial March song",
          "filename": "song_the_imperial_march.ogg",
          "audio_channel_id": 1
        }
      ],

.. important::

   All songs should be played in **channel 1** as explained in
   `audio_channels <#audio-channels-label>`__

.. seealso::

   - The setting `audio_channels <#audio-channels-label>`__
   - `Change channel volume <change_default_settings.html#change-channel-volume-label>`__
   - `Change paths to audio files <change_default_settings.html#change-paths-to-audio-files-label>`__

.. _sound-effects-label:

``sound_effects``
^^^^^^^^^^^^^^^^^
The setting `sound_effects`_ in the configuration file defines the following
sounds:

   - **Breathing sound**: almost as soon as the script :mod:`start_dv` runs,
     Darth Vader's breathing sound starts playing in the background until the
     script ends
   - **Lightsaber drawing sound**: when the lightsaber button is pressed, the
     drawing sound is played first followed by the hum sound which goes on
     until the button is pressed again which will produce the retraction sound
   - **Lightsaber hum sound**: plays immediately after the lightsaber drawing
     sound and goes on until the lightsaber button is pressed again
   - **Lightsaber retraction sound**: plays when the lightsaber button is
     pressed while the hum sound is playing
   - **Closing sound**: plays after the user presses ``ctrl`` + ``c`` to exit
     from the script. By default, it is not played at the end

``sound_effects`` takes a list of sound objects having the following properties:

   - ``id``: this property should **not be modified** because it is
     used to uniquely identify the sound effects
   - ``name``: it is the name of the sound which will be displayed in the
     terminal
   - ``filename``: it is relative to the directory
     `sounds_directory <#sounds-directory-label>`__
   - ``audio_channel_id``: the audio channel used for playing the sound. See
     `audio_channels <#audio-channels-label>`__ to know what channel is used for
     each type of sounds
   - ``mute``: it is only defined for the breathing and closing sounds. If set
     to *true*, the sound will not be played
   - ``loops``: only defined for the breathing sound. It is the number of times
     the sound should be repeated. If set to -1, it will be repeated
     indefinitely

.. code-block:: python
   :emphasize-lines: 6, 14
   :caption: **Example:** two sound effects playing in different audio channels

      "sound_effects": [
        {
          "id": "breathing_sound",
          "name": "Breathing sound",
          "filename": "darth_vader_breathing.ogg",
          "audio_channel_id": 0,
          "mute": false,
          "loops": -1
        },
        {
          "id": "closing_sound",
          "name": "Nooooo [Closing]",
          "filename": "quote_nooooo.ogg",
          "audio_channel_id": 2,
          "mute": true
        }
      ]

.. important::

   The breathing sound should use channel 0, while the other sound effects
   should use channel 2. Hence, the breathing sound can be heard in
   the background while a sound effect is also being played (e.g. the drawing
   sound of the lightsaber). See `audio_channels <#audio-channels-label>`__.

.. seealso::

   - The setting `audio_channels <#audio-channels-label>`__
   - `Change closing sound <change_default_settings.html#change-closing-sound-label>`__
   - `Change paths to audio files <change_default_settings.html#change-paths-to-audio-files-label>`__
   - `Mute breathing sound <change_default_settings.html#mute-breathing-sound-label>`__

.. _sounds_directory-label:

``sounds_directory``
^^^^^^^^^^^^^^^^^^^^
The setting `sounds_directory`_ in the configuration file defines the directory
where all the audio files are saved.

By default, ``sounds_directory`` points to the path where the package
`dv_sounds`_ is installed. `dv_sounds`_ is used to download the various sounds
(e.g. sound efffects) needed for the project.

All the audio filenames found in the configuration file are defined relative to
``sounds_directory``.

.. code-block:: python
   :emphasize-lines: 5
   :caption: **Example:** Filename for the breathing-sound audio file

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

In this example, the audio file `darth_vader_breathing.ogg` is to be found in
the directory ``sounds_directory``.

.. seealso::

   `Change paths to audio files <change_default_settings.html#change-paths-to-audio-files-label>`__

.. _verbose-label:

``verbose``
^^^^^^^^^^^
The setting `verbose`_ in the configuration file is a flag (set to *false* by
default) that allows you to run the script :mod:`start_dv` by logging to the
terminal all messages (logging level is set to DEBUG when ``verbose`` is
*true*). Also, when there is an exception, a traceback is printed so you can
pinpoint exactly where the error occurred in the code which is not the case
when running the script without ``verbose`` (you only get a one-line error
message).

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

   `Script's list of options`_
