.. TODO: check line numbers in URLs (https://github.com/raul23/Darth-Vader-RPi)
.. _audio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L72
.. _gpio_channels: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L8
.. _logging configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_logging_cfg.json
.. _main configuration file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json
.. _mode in the configuration channel: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json#L5
.. _pygame: https://www.pygame.org/docs/
.. _Change GPIO channel names and number: change_default_settings.html#change-gpio-channel-names-and-number
.. _Change keymap: change_default_settings.html#change-keymap
.. _Change LED symbols: change_default_settings.html#change-led-symbols
.. _RPIO.GPIO documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

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

.. _audio-channels-label:

``audio_channels``
^^^^^^^^^^^^^^^^^^

Three audio channels are used for this project:

   - **channel 0**: used for the breathing sound which plays in the background
     as soon as the script runs. Its volume is set by default at 0.2 since we
     don't want to overwhelm the other sounds playing in the other channels.
   - **channel 1**: used for playing the *Imperial March* song and all Darth
     Vader quotes.  Its volume is set by default at 1.0
   - **channel 2**: used for playing the lighsaber sound effects and the closing
     sound. Its volume is set by default at 1.0

The setting `audio_channels`_ in the configuration file defines these three
audio channels with their default volume.

.. code-block:: python
   :emphasize-lines: 4, 8, 12
   :caption: **Audio channels and their default volume**

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

The Python package `pygame`_ is used for playing the various sounds used in this
project.

.. note::

   - Volume takes values in the range 0.0 to 1.0 (inclusive).
   - If value < 0.0, the volume will not be changed
   - If value > 1.0, the volume will be set to 1.0

   As per the `pygame
   documentation <https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.set_volume>`__.

``gpio_channels``
^^^^^^^^^^^^^^^^^
.. TODO: check line # in URL to ``gpio_channels``

The setting `gpio_channels`_ in the configuration file defines the GPIO pins
connected to LEDs and push buttons.

``gpio_channels`` lists GPIO channel objects with the following properties:

   - ``channel_name``: this property should **not be modified** because it is
     used to identify the correct GPIO channel when turning ON/OFF LEDs or
     checking a button's state.
   - ``display_name``: channel name that will be displayed in the terminal
     along with the LED symbol. By default, the channel number is displayed if
     ``display_name`` is not given.
   - ``channel_number``: based on the numbering system you have specified
     (`BOARD` or `BCM`).
   - ``key``: only defined for button objects. It specifies the mapping between
     a keyboard key and a push button so you can simulate push buttons with your
     keyoboard.
   - ``led_symbols``: only defined for LED objects. It is a dictionary defining
     the symbols to be used when the LED is turned ON and OFF.

.. literalinclude:: ../darth_vader_rpi/configs/default_main_cfg.json
   :language: python
   :lines: 8-14, 42-47
   :caption: **Example:** GPIO channels for the lightsaber button and LED

Thus, in this example, you have a push button connected to the GPIO pin 23
(based on the BCM mode) and controlling the lightsaber by turning it ON/OFF
and producing sounds (drawing, closing, and hum sounds). Also, the keyboard
key ``cmd`` simulates the push button when testing the script ``start_dv`` on
your computer.

The ligthsaber LED is connected to GPIO pin 22 (BCM) and is turned ON/OFF when
the corresponding push button (or ``cmd`` key) is pressed.

.. seealso::

   - `Change GPIO channel names and number`_
   - `Change keymap`_
   - `Change LED symbols`_

``mode``
^^^^^^^^
The setting `mode in the configuration channel`_ defines the numbering system
(`BOARD` or `BCM`) used to identify the GPIO channels.

As per the `RPIO.GPIO documentation`_:

``quiet``
^^^^^^^^^

``quotes``
^^^^^^^^^^

``simulation``
^^^^^^^^^^^^^^

``slot_leds``
^^^^^^^^^^^^^

``songs``
^^^^^^^^^

``sound_effects``
^^^^^^^^^^^^^^^^^

``sounds_directory``
^^^^^^^^^^^^^^^^^^^^

``verbose``
^^^^^^^^^^^
