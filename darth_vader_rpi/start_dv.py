#!/usr/bin/env python
"""Script to turn on LEDs and play sound effects on a Raspberry Pi (RPi).

The LEDs illuminate a Darth Vader action figure's lightsaber and the three
slots in the chest control box. 3 push buttons control the following sounds:

1. Some of his famous quotes
2. The Imperial march theme song
3. The lightsaber opening and closing sounds and its illumination

His iconic breathing sound plays in the background indefinitely as soon as the
RPi is run with the script.

The script allows you also to edit the `main config file`_ to setup among other
things the RPi's GPIO pins connected to LEDs and push buttons.

By default the module `RPi.GPIO`_ is used, but if the :ref:`simulation option
(-s) <usage-start-dv-label>` is used with the :mod:`start_dv` script, then the
module `SimulRPi.GPIO`_ will be used instead which simulates `RPi.GPIO`_ for
those that don't have an RPi to test on.

.. _usage-start-dv-label:

Usage
-----

.. highlight:: console

Once the **darth_vader_rpi** package is `installed`_, you should have access to
the :mod:`start_dv` script:

    ``start_dv [-h] [--version] [-q] [-s] [-v] [-e {log,main}] [-a APP]``

Run the script on the RPi with `default values`_ for GPIO channels and other
settings::

    $ start_dv

Run the script using `SimulRPi.GPIO`_ which simulates `RPi.GPIO`_::

    $ start_dv -s

Edit the main config file with *TextEdit* (macOS)::

    $ start_dv -e main -a TextEdit

Edit the logging config file with a default application (e.g. atom)::

    $ start_dv -e log

.. highlight:: python

Notes
-----
More information is available at:

- `Darth-Vader-RPi GitHub <https://github.com/raul23/Darth-Vader-RPi>`_
- `SimulRPi GitHub <https://github.com/raul23/SimulRPi>`_

.. _default values: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json
.. _installed: https://github.com/raul23/Darth-Vader-RPi#readme
.. _logging config file: https://bit.ly/2D6exaD
.. _main config file: https://bit.ly/39x8o3e
.. _pygame.mixer.Sound.play:
    https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.play
.. _RPi.GPIO:
    https://pypi.org/project/RPi.GPIO/
.. _SimulRPi.GPIO: https://github.com/raul23/SimulRPi
.. _YouTube video: https://youtu.be/E2J_xl2MbGU?t=333

"""
# TODO: add PyPi URL in description above (Notes section)

import argparse
import logging.config
import os
import platform
import shutil
import threading
import time
from logging import NullHandler
from threading import Thread

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from darth_vader_rpi import __name__ as package_name, __version__
from darth_vader_rpi.utils import (get_cfg_filepath, override_config_with_args)
# TODO: don't use pytutils
from pyutils.genutils import load_json, run_cmd

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

GPIO = None
""":attr:`GPIO`\'s default value is :obj:`None` and will be eventually set to 
one of the two modules (`RPi.GPIO`_ or `SimulRPi.GPIO`_) depending on the 
user's settings.

`RPi.GPIO`_ provides a class to control the GPIO pins on a Raspberry Pi.

If the `simulation` option (`-s`) is used with the :mod:`start_dv` script, the 
`SimulRPi.GPIO`_ module will be used instead.

"""
_VERBOSE = False
_LOG_CFG = "log_cfg"
_MAIN_CFG = "cfg"
"""TODO"""

_TEST_LOGGING_CFG = None
"""Dictionary containing the logging configuration data.

The default value is :obj:`None` and will be set when performing the tests from
:obj:`darth_vader_rpi.tests`).
"""

_TEST_MAIN_CFG = None
"""Dictionary containing the main configuration data.

The default value is obj:`None` and will be set when performing the tests from
:obj:`darth_vader_rpi.tests`).
"""

_ACTION_MODE = [["top", "middle", "bottom"],
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
                []]
_CALM_MODE = [["middle"],
              ["top"],
              ["middle"],
              ["top"],
              ["middle"],
              ["top"],
              ["top"],
              [],
              ["bottom"],
              []]
"""Darth Vader's physiological status.

These lists represent the sequence the 3 slot LEDs (on his chest box) should be
turned on.  Each item in the list represents a step in the sequence. Thus, in
the case of :attr:`_ACTION_MODE`, all the 3 slot LEDs will be turned on first, 
followed by the top and bottom LEDs, and so on.

An empty subsequence refers to all LEDs being turned off.

References
----------
- Where the sequences were obtained: https://youtu.be/E2J_xl2MbGU?t=333

"""

_SEQ_TYPES_MAP = {'action': _ACTION_MODE, 'calm': _CALM_MODE}
"""TODO
"""


class ExceptionThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.exc = None

    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
            if _VERBOSE:
                logger.exception(_add_spaces_to_msg("Error: {}".format(e)))
            else:
                logger.error(_add_spaces_to_msg("Error: {}".format(e)))


class SoundWrapper:
    """Class that wraps around :class:`pygame.mixer.Channel` and
    :class:`pygame.mixer.Sound`.

    The :meth:`__init__` method takes care of automatically loading the sound
    file. The sound file can then be played or stopped from the specified
    channel `channel_id` with the :meth:`play` or :meth:`stop` method,
    respectively.

    Parameters
    ----------
    sound_id : str
        TODO
    sound_name : str
        Name of the sound file.
    sound_filepath : str
        Path to the sound file.
    channel_id : int
        Channel id associated with an instance of
        :class:`pygame.mixer.Channel` for controlling playback. It must take an
        :obj:`int` value starting from 0.
    play_opening : bool
        TODO
    play_closing : bool
        TODO

    .. note::

        It is a wrapper with a very minimal interface to
        :class:`pygame.mixer.Channel` where only two methods :meth:`play` and
        :meth:`stop` are provided for the sake of the project.

    """

    def __init__(self, sound_id, sound_name, sound_filepath, channel_id,
                 play_opening=False, play_closing=False):
        self.sound_id = sound_id
        self.sound_name = sound_name
        self.sound_filepath = sound_filepath
        self.channel_id = channel_id
        self.play_opening = play_opening
        self.play_closing = play_closing
        self._channel = pygame.mixer.Channel(channel_id)
        # Load sound file
        self._pygame_sound = pygame.mixer.Sound(self.sound_filepath)

    def play(self, loops=0):
        """Play a sound on the specified Channel `channel_id`.

        Parameters
        ----------
        loops : int
            Controls how many times the sample will be repeated after being
            played the first time. The default value (zero) means the sound is
            not repeated, and so is only played once. If `loops` is set to -1
            the sound will loop indefinitely (though you can still call
            :meth:`stop` to stop it). Reference from
            :meth:`pygame.mixer.Sound.play`.

        """
        self._channel.play(self._pygame_sound, loops)

    def stop(self):
        """Stop playback on the specified channel `channel_id`.
        """
        self._channel.stop()
        self._channel.stop()


# TODO: clear buffer
# TODO: add description
def _add_spaces_to_msg(msg, nb_spaces=60):
    return "{}{}".format(msg, " " * nb_spaces)


# TODO: add description
def _get_cfg_dict(cfg_type):
    global_cfg = {'main': _TEST_MAIN_CFG,
                  'log': _TEST_LOGGING_CFG
                  }
    if global_cfg[cfg_type]:
        # Performing tests-suite
        cfg_dict = global_cfg[cfg_type]
    else:
        cfg_filepath = get_cfg_filepath(cfg_type)
        try:
            cfg_dict = load_json(cfg_filepath)
        except FileNotFoundError:
            # Config file not found
            # Copy it from the default one
            default_cfg_type = "default_{}".format(cfg_type)
            src = get_cfg_filepath(default_cfg_type)
            shutil.copy(src, cfg_filepath)
            cfg_dict = load_json(cfg_filepath)
    return cfg_dict


def turn_on_slot_leds_sequence(top_led, middle_led, bottom_led,
                               leds_sequence="action", delay_subsequences=0.4,
                               time_leds_on=0.4):
    """Turn on/off the three slot LEDs in a precise sequence.

    These three LEDs are associated with Darth Vader's three slots located on
    his chest control box. These LEDs are labeled as 'top_led', 'middle_led',
    and 'bottom_led', respectively.

    The three LEDs are turned on according to a default or custom sequence
    which repeats itself. The default values for `leds_sequence` are 'action'
    and 'calm' which represent Darth Vader's physiological state as a sequence
    of LEDs blinking in a particular order.

    The user can also provide its own `leds_sequence` by using a list of LED
    labels {'top', 'midddle', 'bottom'} arranged in a sequence as to specify
    the order the slot LEDs should turn on/off, e.g. ``[['top', 'bottom'], [],
    ['middle'], []]`` will turn on/off the slot LEDs in this order::

        1. top + bottom LEDs turned on
        2. All LEDs turned off
        3. middle LED turned on
        4. All LEDs turned off

    The LEDs will be turned on for `time_leds_on` seconds.

    There will be a delay of `delay_subsequences` seconds between
    subsequences of LEDs being turned on, i.e. between each step in the
    previous example.

    The default sequences of slot LEDs were obtained from this
    `YouTube video`_.

    Parameters
    ----------
    top_led : int
        TODO
    middle_led : int
        TODO
    bottom_led : int
        TODO
    leds_sequence : str or list, optional
        Sequence of slot LEDs on Darth Vader's chest box.

        If `leds_sequence` is a string, then it takes on one of these values
        which represent Darth Vader's physiological state: {'action', 'calm'}.

        If `leds_sequence` is a list, then it must be a list of slot LED labels
        {'top', 'midddle', 'bottom'} arranged in a sequence as to specify the
        order the slot LEDs should turn on/off, e.g. ``[['top', 'bottom'], [],
        ['middle'], []]`` will turn on/off the slot LEDs in this order::

            1. top + bottom LEDs turn on
            2. All LEDs turn off
            3. middle LED turn on
            4. All LEDs turn off

    delay_subsequences : float, optional
        Delay in seconds between subsequences of LEDs. The default value is 0.4
        seconds.
    time_leds_on : float, optional
        Time in seconds the LEDs will be turned on. The default value is 0.4
        seconds.

        .. important::

            This also affects the time all LEDs will remain turned off if a
            subsequence in `leds_sequence` is an empty list.


    .. important::

        :meth:`turn_on_slot_leds_sequence` should be run by a thread and
        eventually stopped from the main thread by setting its ``do_run``
        attribute to `False` to let the thread exit from its target function.

        **For example**:

        .. code-block:: python

            th = threading.Thread(target=turn_on_slot_leds_sequence,
                                  args=(leds_channels))
            th.start()

            # Your other code ...

            # Time to stop thread
            th.do_run = False
            th.join()

    """
    lcm = dict((('top', top_led), ('middle', middle_led), ('bottom', bottom_led)))
    if isinstance(leds_sequence, str):
        leds_sequence = leds_sequence.lower()
        assert leds_sequence in _SEQ_TYPES_MAP.keys(), \
            "Wrong type of leds_sequence: '{}' (choose from {})".format(
                leds_sequence, ", ".join(_SEQ_TYPES_MAP.keys()))
        leds_sequence = _SEQ_TYPES_MAP[leds_sequence]
    else:
        assert isinstance(leds_sequence, list), \
            "leds_sequence should be a string ({}) or a list: '{}'".format(
                ", ".join(_SEQ_TYPES_MAP.keys()), leds_sequence)
    th = threading.currentThread()
    subseq_idx = 0
    while getattr(th, "do_run", True):
        leds_subsequence = leds_sequence[subseq_idx % len(leds_sequence)]
        subseq_idx += 1
        for channel_label in leds_subsequence:
            channel = lcm[channel_label]
            turn_on_led(channel)
        time.sleep(time_leds_on)
        if leds_subsequence:
            turn_off_led(lcm['top'])
            turn_off_led(lcm['middle'])
            turn_off_led(lcm['bottom'])
            time.sleep(delay_subsequences)
    logger.debug(_add_spaces_to_msg("Stopping thread: {}".format(th.name)))


def turn_off_led(channel):
    """Turn off a LED from a given channel.

    Parameters
    ----------
    channel : int
        Channel number associated with a LED which will be turned off.

    """
    # logger.debug("LED {} off".format(led))
    GPIO.output(channel, GPIO.LOW)


def turn_on_led(channel):
    """Turn on a LED from a given channel.

    Parameters
    ----------
    channel : int
        Channel number associated with a LED which will be turned on.

    """
    # logger.debug("LED {} on".format(led))
    GPIO.output(channel, GPIO.HIGH)


def activate_dv(main_cfg):
    """Activate Darth Vader by turning on LEDs and playing sounds.

    The LEDs illuminate Darth Vader's lightsaber and the three slots in the
    chest control box. 3 push buttons control the following sounds:

    1. Some of his famous quotes
    2. The Imperial march theme song
    3. The lightsaber opening and closing sounds and its illumination

    His iconic breathing sound plays in the background indefinitely as soon as
    the RPi is run with the script.

    While the function waits for a pressed button, you can exit from this
    function by pressing :obj:`ctr` + :obj:`c`.

    Parameters
    ----------
    main_cfg : dict
        Dictionary containing the configuration data to setup the RPi, such as
        the GPIO pins and the sound files. See `main config file`_ for a
        detailed look into its content.

    Returns
    -------
    retcode: int
        If the function is run without any :exc:`Exception`, the return code is
        0. Otherwise, it is 1.

        Also, even if there is an :exc:`Exception`, we will try to clean up
        before exiting from the function.

    """
    retcode = 0
    th_slot_leds = None
    gpio_channels = {}
    loaded_sounds = {}
    try:
        logger.info("pygame mixer initialization")
        pygame.mixer.init()
        logger.info("RPi initialization")
        GPIO.setmode(GPIO.MODES[main_cfg['mode'].upper()])
        GPIO.setwarnings(False)
        # Setup LEDs and buttons
        for gpio_ch in main_cfg['gpio_channels']:
            if gpio_ch['channel_id'].endswith("_led"):
                # LEDs
                GPIO.setup(gpio_ch['channel_number'], GPIO.OUT)
            else:
                # Buttons
                GPIO.setup(gpio_ch['channel_number'], GPIO.IN,
                           pull_up_down=GPIO.PUD_UP)
            gpio_channels[gpio_ch['channel_id']] = {
                'channel_number': gpio_ch['channel_number'],
                'channel_name': gpio_ch['channel_name'],
                'key': gpio_ch.get('key'),
                'led_symbol': gpio_ch.get('led_symbols')
            }

        ### Sound
        # Create separate channel
        # Ref.: stackoverflow.com/a/59742418
        audio_channels = main_cfg['audio_channels']
        for ch_dict in audio_channels:
            channel = pygame.mixer.Channel(ch_dict['channel_id'])
            channel.set_volume(ch_dict['volume'])

        sounds_dir = os.path.expanduser(main_cfg['sounds_directory'])

        logger.info("")
        # Load sounds from cfg
        for sound_type in ['quotes', 'songs', 'sound_effects']:
            logger.info('Loading {}...'.format(sound_type.replace("_", " ")))
            for sound in main_cfg[sound_type]:
                sound_id = sound['id']
                sound_name = sound['name']
                logger.info('Loading "{}"'.format(sound_name))
                filepath = os.path.join(sounds_dir, sound['filename'])
                sw = SoundWrapper(
                    sound_id=sound_id,
                    sound_name=sound_name,
                    sound_filepath=filepath,
                    channel_id=sound['audio_channel_id'],
                    play_opening=sound.get('play_opening', False),
                    play_closing=sound.get('play_closing', False))
                if sound_type == "quotes":
                    loaded_sounds.setdefault("quotes", {})
                    loaded_sounds['quotes'].setdefault(sound_id, sw)
                else:
                    loaded_sounds.setdefault(sound_id, sw)
                if sw.play_opening:
                    loops = sound.get('loops', 0)
                    loaded_sounds[sound_id].play(loops)
            logger.info("")
        quotes = list(loaded_sounds['quotes'].values())
        th_slot_leds = ExceptionThread(
            name="thread_slot_leds",
            target=turn_on_slot_leds_sequence,
            args=(gpio_channels['top_led']['channel_number'],
                  gpio_channels['middle_led']['channel_number'],
                  gpio_channels['bottom_led']['channel_number'],
                  main_cfg['slot_leds']['sequence'],
                  main_cfg['slot_leds']['delay_subsequences'],
                  main_cfg['slot_leds']['time_leds_on']))

        th_slot_leds.start()
        logger.info("")
        logger.info(_add_spaces_to_msg("Press buttons"))
        pressed_lightsaber = False
        quote_idx = 0

        while True:
            if not GPIO.input(gpio_channels['lightsaber_button']['channel_number']):
                # logger.debug("\n\nButton {} pressed...".format(
                    # lightsaber_button))
                if pressed_lightsaber:
                    pressed_lightsaber = False
                    loaded_sounds['lightsaber_retraction_sound'].play()
                    time.sleep(0.1)
                    turn_off_led(22)
                else:
                    pressed_lightsaber = True
                    loaded_sounds['lightsaber_drawing_sound'].play()
                    loaded_sounds['lightsaber_hum_sound'].play(-1)
                    time.sleep(0.1)
                    turn_on_led(gpio_channels['lightsaber_led']['channel_number'])
                time.sleep(0.2)
            elif not GPIO.input(gpio_channels['song_button']['channel_number']):
                # logger.debug("\n\nButton {} pressed...".format(song_button))
                loaded_sounds['imperial_march_song'].play()
                time.sleep(0.2)
            elif not GPIO.input(gpio_channels['quotes_button']['channel_number']):
                """
                logger.debug("\n\nButton {} pressed...".format(
                    gpio_channels['quotes_button']['channel_name']))
                """
                quote = quotes[quote_idx % len(quotes)]
                quote_idx += 1
                quote.play()
                time.sleep(0.2)
            elif not th_slot_leds.is_alive():
                retcode = 1
                logger.info(_add_spaces_to_msg("Exiting..."))
                break
    except Exception as e:
        retcode = 1
        if main_cfg['verbose']:
            logger.exception(_add_spaces_to_msg("Error: {}".format(e)))
        else:
            logger.error(_add_spaces_to_msg(e.__repr__()))
        logger.info(_add_spaces_to_msg("Exiting..."))
    except KeyboardInterrupt:
        logger.info(_add_spaces_to_msg("Exiting..."))
        closing_sound = loaded_sounds.get('closing_sound')
        if closing_sound and closing_sound.play_closing:
            closing_sound.play()
            time.sleep(1)

    GPIO.setprinting(False)
    if gpio_channels:
        for channel_id, channel_info in gpio_channels.items():
            if channel_id.endswith("_led"):
                turn_off_led(channel_info['channel_number'])
    if th_slot_leds:
        logger.debug(_add_spaces_to_msg("Stopping thread ..."))
        th_slot_leds.do_run = False
        th_slot_leds.join()
        logger.debug(_add_spaces_to_msg("Thread stopped: {}".format(th_slot_leds.name)))
    for ch in main_cfg['audio_channels']:
        pygame.mixer.Channel(ch['channel_id']).stop()
    logger.info(_add_spaces_to_msg("Cleanup..."))
    GPIO.cleanup()

    return retcode


def edit_config(cfg_type, app=None):
    """Edit a configuration file.

    The user chooses what type of config file (`cfg_type`) to edit: 'log' for
    the `logging config file`_ and 'main' for the `main config file`_.

    The configuration file can be opened by a user-specified application (`app`)
    or a default program associated with this type of file (when `app` is
    :obj:`None`).

    Parameters
    ----------
    cfg_type : str, {'log', 'main'}
        The type of configuration file we want to edit. 'log' refers to the
        `logging config file`_, and 'main' to the `main config file`_ used to
        setup the Darth-Vader-RPi project such as specifying the sound effects
        or the GPIO channels.
    app : str
        Name of the application to use for opening the config file, e.g. 
        `TextEdit` (the default value is :obj:`None` which implies that the
        default application will be used to open the config file).

    Returns
    -------
    retcode : int
        If there is a `subprocess
        <https://docs.python.org/3/library/subprocess.html#subprocess.CalledProcessError>`_
        -related error, the return code is non-zero. Otherwise, it is 0 if the
        file can be successfully opened with an external program.

    """
    # Get path to user-defined config file
    filepath = get_cfg_filepath(cfg_type)
    # Command to open the config file with the default application in the
    # OS or the user-specified app, e.g. `open filepath` in macOS opens the
    # file with the default app (e.g. atom)
    default_cmd_dict = {'Darwin': 'open {filepath}',
                        'Linux': 'xdg-open {filepath}',
                        'Windows': 'cmd /c start "" "{filepath}"'}
    # NOTE: check https://bit.ly/31htaOT (pymotw) for output from
    # platform.system on three OSes
    default_cmd = default_cmd_dict.get(platform.system())
    # NOTES:
    # - `app is None` implies that the default app will be used
    # - Otherwise, the user-specified app will be used
    cmd = default_cmd if app is None else app + " " + filepath
    retcode = 1
    result = None
    try:
        # IMPORTANT: if the user provided the name of an app, it will be used as
        # a command along with the file path, e.g. `$ atom {filepath}`. However,
        # this case might not work if the user provided an app name that doesn't
        # refer to an executable, e.g. `$ TextEdit {filepath}` won't work. The
        # failed case is further processed in `except FileNotFoundError`.
        result = run_cmd(cmd.format(filepath=filepath))
        retcode = result.returncode
    except FileNotFoundError:
        # This error happens if the name of the app can't be called as an
        # executable on the terminal
        # e.g. TextEdit can't be run on the terminal but atom can since the
        # latter refers to an executable.
        # To open TextEdit from the terminal, the command `open -a TextEdit`
        # must be used on macOS.
        # TODO: add the open commands for the other OSes
        specific_cmd_dict = {'Darwin': 'open -a {app}'.format(app=app)}
        # Get the command to open the file with the user-specified app
        cmd = specific_cmd_dict.get(platform.system(), app) + " " + filepath
        # TODO: explain DEVNULL, suppress stderr since we will display the error
        result = run_cmd(cmd)  # stderr=subprocess.DEVNULL)
        retcode = result.returncode
    if retcode == 0:
        logger.info("Opening the {} configuration file ...".format(cfg_type))
    else:
        if result:
            err = result.stderr.decode().strip()
            logger.error(err)
    return retcode


def setup_argparser():
    """Setup the argument parser for the command-line script.

    The important actions that can be performed with the script are:

    - activate Darth Vader (turn on LEDs and play sound effects),
    - edit a configuration file or
    - reset/undo a configuration file *[SOON]*.

    Returns
    -------
    parser : argparse.ArgumentParser
        Argument parser.

    """
    # Help message that is used in various arguments
    common_help = '''Provide '{}' for the logging config file or '{}' for the 
    main config file.'''.format(_LOG_CFG, _MAIN_CFG)
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        # prog=os.path.basename(__file__),
        description='''\
Activate Darth Vader by turning on LEDs on his suit and lightsaber, and by 
pressing buttons to produce sound effects.\n
IMPORTANT: these are only some of the most important options. Open the main 
config file to have access to the complete list of options, i.e. 
%(prog)s -e {}'''.format(_MAIN_CFG),
        # formatter_class=argparse.RawDescriptionHelpFormatter)
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # ===============
    # General options
    # ===============
    parser.add_argument("--version", action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Enable quiet mode, i.e. nothing will be printed.")
    parser.add_argument("-s", "--simulation", action="store_true",
                        help="Enable simulation mode, i.e. SimulRPi.GPIO will "
                             "be used for simulating RPi.GPIO.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print various debugging information, e.g. print "
                             "traceback when there is an exception.")
    # Group arguments that are closely related
    # ===========
    # Edit config
    # ===========
    edit_group = parser.add_argument_group('Edit a configuration file')
    edit_group.add_argument(
        "-e", "--edit", choices=[_LOG_CFG, _MAIN_CFG],
        help="Edit a configuration file. {}".format(common_help))
    edit_group.add_argument(
        "-a", "--app-name", dest="app",
        help='''Name of the application to use for editing the file. If no 
            name is given, then the default application for opening this type of
            file will be used.''')
    # =================
    # Reset/Undo config
    # =================
    """
    reset_group = parser.add_argument_group(
        'Reset or undo a configuration file')
    reset_group.add_argument(
        "-r", "--reset", choices=[_LOG_CFG, _MAIN_CFG],
        help='''Reset a configuration file with factory default values. 
            {}'''.format(common_help))
    reset_group.add_argument(
        "-u", "--undo", choices=[_LOG_CFG, _MAIN_CFG],
        help='''Undo the LAST RESET. Thus, the config file will be restored 
            to what it was before the LAST reset. {}'''.format(common_help))
    
    """
    return parser


def main():
    """Main entry-point to the script.

    According to the user's choice of action, the script might:

    - activate Darth Vader,
    - edit a configuration file, or
    - reset/undo a configuration file *[SOON]*.

    Notes
    -----
    Only one action at a time can be performed.

    """
    global logger, GPIO, _VERBOSE
    # Setup the default logger (whose name is __main__ since this file is run
    # as a script) which will be used for printing to the console before all
    # loggers defined in the JSON file will be configured. The printing with
    # this default logger will only be done in the cases that the user allows
    # it, e.g. the verbose option is enabled.
    # IMPORTANT: the config options need to be read before using any logger
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    parser = setup_argparser()
    args = parser.parse_args()

    # Get main config dict
    main_cfg_dict = _get_cfg_dict('main')

    # Override logging configuration with command-line arguments
    retval = override_config_with_args(main_cfg_dict, parser)

    # ==============
    # Logging config
    # ==============
    # NOTE: if quiet and verbose are both activated, only quiet will have an
    # effect
    if main_cfg_dict['quiet']:
        logger.disabled = True
    else:
        # Setup logger
        logging_cfg_dict = _get_cfg_dict('log')
        # TODO: sanity check on loggers (names based in package...)
        if main_cfg_dict['verbose']:
            _VERBOSE = True
            keys = ['handlers', 'loggers']
            for k in keys:
                for name, val in logging_cfg_dict[k].items():
                    val['level'] = "DEBUG"
        logging.config.dictConfig(logging_cfg_dict)
        logger_name = "{}.{}".format(
            package_name,
            os.path.splitext(__file__)[0])
        logger = logging.getLogger(logger_name)
        logger.info("Verbose option {}".format(
            "enabled" if main_cfg_dict['verbose'] else "disabled"))
        msg1 = "Config options overriden by command-line arguments:\n"
        for cfg_name, old_v, new_v in retval.config_opts_overidden:
            msg1 += "{}: {} --> {}\n".format(cfg_name, old_v, new_v)
        msg2 = "Command-line arguments not found in JSON config file: " \
               "{}".format(retval.args_not_found)
        logger.debug(msg1)
        logger.debug(msg2)

    # =======
    # Actions
    # =======
    retcode = 0
    # TODO: enlarge try? even if logger not setup completely
    try:
        if args.edit:
            if args.edit == _MAIN_CFG:
                args.edit = "main"
            elif args.edit == _LOG_CFG:
                args.edit = "log"
            else:
                raise ValueError(
                    "edit argument not valid: '{}' (choose from {})".format(
                        args.edit,
                        ", ".join("'{}'".format(i) for i in [_LOG_CFG,
                                                             _MAIN_CFG])))
            retcode = edit_config(args.edit, args.app)
            """
            elif args.reset:
                retcode = reset_config(args.reset)
            elif args.undo:
                retcode = undo_config(args.undo)
            """
        else:
            if main_cfg_dict['simulation']:
                import SimulRPi.GPIO as GPIO
                GPIO.setchannels(main_cfg_dict['gpio_channels'])
                GPIO.setprinting(not main_cfg_dict['quiet'])
                logger.info("Simulation mode enabled")
            else:
                import RPi.GPIO as GPIO
            # TODO: works on UNIX shell only, not Windows
            # ref.: https://bit.ly/3f3A7dc
            # os.system("tput civis")
            retcode = activate_dv(main_cfg_dict)
    except Exception as e:
        # TODO: explain this line
        # traceback.print_exc()
        if args.verbose:
            logger.exception(e)
        else:
            # logger.error(e.__repr__())
            # TODO: add next line in a utility function
            err_msg = "{}: {}".format(str(e.__class__).split("'")[1], e)
            logger.error(err_msg)
        retcode = 1
    finally:
        # TODO: works on UNIX shell only, not Windows
        # os.system("tput cnorm")
        if main_cfg_dict['quiet']:
            print()
        return retcode


if __name__ == '__main__':
    retcode = main()
    msg = "Program exited with {}".format(retcode)
    if retcode == 1:
        logger.error(msg)
    else:
        logger.info(msg)
