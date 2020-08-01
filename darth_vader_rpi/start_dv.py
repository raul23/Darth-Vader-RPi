#!/usr/script/env python
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
(-s) <usage-start-dv-Label>` is used with the :mod:`start_dv` script, then the
module `SimulRPi.GPIO`_ will be used instead which simulates `RPi.GPIO`_ for
those that don't have an RPi to test on.

.. _usage-start-dv-Label:

Usage
-----

Once the `darth_vader_rpi` package is `installed`_, you should have access to
the :mod:`start_dv` script:

    ``start_dv [-h] [--version] [-q] [-s] [-v] [-e {log,main}] [-a APP]``

Run the script on the RPi::

    $ start_dv

Run the script using `SimulRPi.GPIO`_ which simulates RPi.GPIO::

    $ start_dv -s

Edit the main config file with *TextEdit* (macOS)::

    $ start_dv -e main -a TextEdit

Edit the logging config file with a default application (e.g. atom)::

    $ start_dv -e log

Notes
-----
More information is available at:

- Darth-Vader-RPi GitHub: https://github.com/raul23/Darth-Vader-RPi
- SimulRPi GitHub: https://github.com/raul23/SimulRPi

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
import threading
import time
from logging import NullHandler

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from darth_vader_rpi import __name__ as package_name, __version__
from darth_vader_rpi.utils import (get_cfg_filepath, override_config_with_args)
from pyutils.genutils import load_json, run_cmd

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

GPIO = None
"""`RPi.GPIO`_ provides a class to control the GPIO pins on a Raspberry Pi.

If the `simulation` option (`-s`) is used with the :mod:`start_dv` script, the 
`SimulRPi.GPIO`_ module will be used instead. :attr:`GPIO`\'s default value is 
:obj:`None` and will be eventually set to one of the two modules (`RPi.GPIO`_ 
or `SimulRPi.GPIO`_) depending on the user's settings.

"""

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

_VALID_SEQ_TYPES = ["calm", "active"]
"""TODO
"""

_ACTIVE_MODE = [["top", "middle", "bottom"],
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
the case of :attr:`_ACTIVE_MODE`, all the 3 slot LEDs will be turned on first, 
followed by the top and bottom LEDs, and so on.

An empty subsequence refers to all LEDs being turned off.

References
----------
- Where the sequences were obtained: https://youtu.be/E2J_xl2MbGU?t=333

"""


class SoundWrapper:
    """Class that wraps around :class:`pygame.mixer.Channel` and
    :class:`pygame.mixer.Sound`.

    The :meth:`__init__` method takes care of automatically loading the sound
    file. The sound file can then be played or stopped from the specified
    channel `channel_id` with the :meth:`play` or :meth:`stop` method,
    respectively.

    Parameters
    ----------
    sound_name : str
        Name of the sound file.
    sound_filepath : str
        Path to the sound file.
    channel_id : int
        Channel id associated with an instance of
        :class:`pygame.mixer.Channel` for controlling playback. It must take an
        :obj:`int` value starting from 0.


    .. note::

        It is a wrapper with a very minimal interface to
        :class:`pygame.mixer.Channel` where only two methods :meth:`play` and
        :meth:`stop` are provided for the sake of the project.

    """

    def __init__(self, sound_name, sound_filepath, channel_id):
        self.sound_name = sound_name
        self.sound_filepath = sound_filepath
        self.channel_id = channel_id
        self._channel = pygame.mixer.Channel(channel_id)
        # Load sound file
        self._pygame_sound = pygame.mixer.Sound(self.sound_filepath)

    def play(self, loops=0):
        """Play a Sound on the specified Channel `channel_id`.

        Parameters
        ----------
        loops : int
            Controls how many times the sample will be repeated after being
            played the first time. The default value (zero) means the aound is
            not repeated, and so is only played once. If `loops` is set to -1
            the Sound will loop indefinitely (though you can still call
            :meth:`stop` to stop it). Reference from
            :meth:`pygame.mixer.Sound.play`.

        """
        self._channel.play(self._pygame_sound, loops)

    def stop(self):
        """Stop playback on the specified channel `channel_id`.
        """
        self._channel.stop()


# TODO: clear buffer
def _add_spaces_to_msg(msg, nb_spaces=20):
    return "{}{}".format(msg, " " * nb_spaces)


def _get_cfg_dict(cfg_type):
    global_cfg = {'main': _TEST_MAIN_CFG,
                  'log': _TEST_LOGGING_CFG
                  }
    # Load main config file
    if global_cfg[cfg_type]:
        cfg_dict = global_cfg[cfg_type]
    else:
        cfg_filepath = get_cfg_filepath(cfg_type)
        cfg_dict = load_json(cfg_filepath)
    return cfg_dict


def turn_on_slot_leds_sequence(leds_channels_map, leds_sequence="active",
                               delay_between_leds_on=0.4, time_leds_on=0.4,):
    """Turn on/off three slot LEDs in a precise sequence.

    These three LEDs are associated with Darth Vader's three slots located on
    his chest control box. These three LEDs are labeled as 'top', 'middle', and
    'bottom' in the `leds_channels_map` dictionary.

    The three LEDs are turn on according to a default or custom sequence which
    repeats itself. The default `leds_sequence` are 'active' and 'calm' which
    represent Darth Vader's physiological state.

    The user can also provide its own `leds_sequence` by using a list of LED
    labels {'top', 'midddle', 'bottom'} arranged in a sequence as to specify
    the order the slot LEDs should turn on/off, e.g. ``[['top', 'bottom'], [],
    ['middle'], []]`` will turn on/off the slot LEDs in this order::

        1. top + bottom LEDs turn on
        2. All LEDs turn off
        3. middle LED turn on
        4. All LEDs turn off

    The LEDs will be turned on for `time_leds_on` seconds.

    There will be a delay of `delay_between_leds_on` seconds between
    subsequences of LEDs being turn on, i.e. between each step in the previous
    example.

    The default sequences of slot LEDs were obtained from this `YouTube video`_.

    Parameters
    ----------
    leds_channels_map : dict
        Dictionary mapping the type of slot LED {'top', 'middle', 'bottom'} and 
        its channel id (:obj:`int`).

    leds_sequence : str or list, optional
        Sequence of slot LEDs on Darth Vader's chest box.

        If `leds_sequence` is a string, then it takes on one of these values
        which represent Darth Vader's physiological state: {'active', 'calm'}.

        If `leds_sequence` is a list, then it must be a list of slot LED labels
        {'top', 'midddle', 'bottom'} arranged in a sequence as to specify the
        order the slot LEDs should turn on/off, e.g. ``[['top', 'bottom'], [],
        ['middle'], []]`` will turn on/off the slot LEDs in this order::

            1. top + bottom LEDs turn on
            2. All LEDs turn off
            3. middle LED turn on
            4. All LEDs turn off

    delay_between_leds_on : float, optional
        Delay in seconds between subsequences of LEDs. The default value is 0.4
        seconds.

    time_leds_on : float, optional
        Time in seconds the LEDs will be turned on. The default value is 0.4
        seconds.

        .. important::

            This also affects the time all LEDs will remain turn off if a
            subsequence in `leds_sequence` is an empty list.


    .. important::

        :meth:`turn_on_slot_leds_sequence` should be run by a thread and
        eventually stopped from the main thread by setting its ``do_run``
        attribute to *False* to let the thread exit its target function.

        .. code-block:: python

            th = threading.Thread(target=turn_on_slot_leds_sequence,
                                  args=(leds_channels))
            th.start()

            # Your other code ...

            # Time to stop thread
            th.do_run = False
            th.join()

    """
    lcm = leds_channels_map
    if isinstance(leds_sequence, str):
        assert leds_sequence in _VALID_SEQ_TYPES, \
            "Wrong type of leds_sequence: '{}' (choose from {})".format(
                leds_sequence, ", ".join(_VALID_SEQ_TYPES))
    else:
        assert isinstance(leds_sequence, list), \
            "leds_sequence should be a string ({}) or a list: '{}'".format(
                ", ".join(_VALID_SEQ_TYPES), leds_sequence)
    t = threading.currentThread()
    if leds_sequence == "calm":
        leds_sequence = _CALM_MODE
    elif leds_sequence == "active":
        leds_sequence = _ACTIVE_MODE
    subseq_idx = 0
    while getattr(t, "do_run", True):
        leds_subsequence = leds_sequence[subseq_idx % len(leds_sequence)]
        subseq_idx += 1
        for channel_label in leds_subsequence:
            channel = leds_channels_map[channel_label]
            turn_on_led(channel)
        time.sleep(time_leds_on)
        if leds_subsequence:
            turn_off_led(lcm['top'])
            turn_off_led(lcm['middle'])
            turn_off_led(lcm['bottom'])
            time.sleep(delay_between_leds_on)
    logger.info("Stopping thread: {}()".format(
        turn_on_slot_leds_sequence.__name__))


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

    Parameters
    ----------
    main_cfg : dict
        Dictionary containing the configuration data to setup the RPi, such as
        the GPIO pins and the sound files. See `main config file`_ for a
        detailed look into its content.

    Returns
    -------
    retcode: int
        If the script is run on the RPi without any :exc:`Exception`, the
        return code is 0. Otherwise, it is 1.

    """
    logger.info("pygame mixer initialization")
    pygame.mixer.init()
    logger.info("RPi initialization")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # LEDs
    top_led = main_cfg['GPIO']['top_led']
    middle_led = main_cfg['GPIO']['middle_led']
    bottom_led = main_cfg['GPIO']['bottom_led']
    lightsaber_led = main_cfg['GPIO']['lightsaber_led']
    GPIO.setup(top_led, GPIO.OUT)
    GPIO.setup(middle_led, GPIO.OUT)
    GPIO.setup(bottom_led, GPIO.OUT)
    GPIO.setup(lightsaber_led, GPIO.OUT)
    # Buttons
    lightsaber_button = main_cfg['GPIO']['lightsaber_button']
    song_button = main_cfg['GPIO']['song_button']
    quotes_button = main_cfg['GPIO']['quotes_button']
    GPIO.setup(lightsaber_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(song_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(quotes_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    ### Sound
    # Create separate channel
    # Ref.: stackoverflow.com/a/59742418
    channels = main_cfg['channels']
    for ch_dict in channels:
        channel = pygame.mixer.Channel(ch_dict['channel_id'])
        channel.set_volume(ch_dict['volume'])

    loaded_sounds = {}
    sounds_dir = os.path.expanduser(main_cfg['sounds_directory'])
    logger.info("Loading sound effects...")

    def load_sounds():
        for sound_type in ['quotes', 'songs', 'sound_effects']:
            if sound_type == 'quotes':
                for quote in main_cfg[sound_type]:
                    logger.info("Loading {}".format(quote['name']))
                    loaded_sounds.setdefault('quotes', [])
                    filepath = os.path.join(sounds_dir, quote['filename'])
                    loaded_sounds['quotes'].append(
                        SoundWrapper(sound_name=quote['name'],
                                     sound_filepath=filepath,
                                     channel_id=quote['channel_id']))
            elif sound_type in ['songs', 'sound_effects']:
                for s in main_cfg[sound_type]:
                    sound = s.popitem()
                    sound_name = sound[0]
                    sound_info = sound[1]
                    logger.info("Loading {}".format(sound[0]))
                    filepath = os.path.join(sounds_dir, sound_info['filename'])
                    sw = SoundWrapper(sound_name=sound_name,
                                      sound_filepath=filepath,
                                      channel_id=sound_info['channel_id'])
                    loaded_sounds.setdefault(sound_name, sw)
                    if sound_info.get('play'):
                        loops = sound_info.get('loops', -1)
                        loaded_sounds[sound_name].play(loops)

    load_sounds()
    quotes = loaded_sounds['quotes']

    leds_channels = {'top': top_led, 'middle': middle_led, 'bottom': bottom_led}
    th = threading.Thread(target=turn_on_slot_leds_sequence, 
                          args=(leds_channels,
                                main_cfg['slot_leds']['sequence'],
                                main_cfg['slot_leds']['delay_between_leds_on'],
                                main_cfg['slot_leds']['time_leds_on']))
    th.start()

    logger.info("")
    logger.info(_add_spaces_to_msg("Press any button"))
    pressed_lightsaber = False
    quote_idx = 0

    retcode = 0
    try:
        while True:
            if not GPIO.input(lightsaber_button):
                logger.debug("\n\nButton {} pressed...".format(
                    lightsaber_button))
                if pressed_lightsaber:
                    pressed_lightsaber = False
                    loaded_sounds['lightsaber_close_sound'].play()
                    time.sleep(0.1)  # 0.3
                    turn_off_led(22)
                else:
                    pressed_lightsaber = True
                    loaded_sounds['lightsaber_open_sound'].play()
                    loaded_sounds['lightsaber_running_sound'].play(-1)
                    time.sleep(0.1)  # 0.3
                    turn_on_led(lightsaber_led)
                time.sleep(0.2)  # 0.2
            elif not GPIO.input(song_button):
                logger.debug("\n\nButton {} pressed...".format(song_button))
                loaded_sounds['imperial_march_song'].play()
                time.sleep(0.2)
            elif not GPIO.input(quotes_button):
                logger.debug("\n\nButton {} pressed...".format(quotes_button))
                quote = quotes[quote_idx % len(quotes)]
                quote_idx += 1
                quote.play()
                time.sleep(0.2)
    except Exception as e:
        logger.exception(_add_spaces_to_msg("Error: {}".format(e)))
        logger.info(_add_spaces_to_msg("Exiting..."))
        retcode = 1
    except KeyboardInterrupt:
        logger.info(_add_spaces_to_msg("Exiting..."))

    logger.info(_add_spaces_to_msg("Cleanup..."))
    for gpio_name, gpio_pin in main_cfg['GPIO'].items():
        if gpio_name.endswith("_led"):
            turn_off_led(gpio_pin)
    GPIO.cleanup()
    th.do_run = False
    th.join()
    for ch in main_cfg['channels']:
        pygame.mixer.Channel(ch['channel_id']).stop()

    return retcode


def edit_config(cfg_type, app=None):
    """Edit a configuration file.

    The user chooses what type of config file (`cfg_type`) to edit: 'log' for
    the `logging config file`_ and 'main' for the `main config file`_.

    The configuration file can be opened by a user-specified application (`app`)
    or a default program associated with this type of file (when `app` is None).

    Parameters
    ----------
    cfg_type : str, {'log', 'main'}
        The type of configuration file we want to edit. 'log' refers to the
        `logging config file`_, and 'main' to the `main config file`_ used to
        setup the Darth-Vader-RPi project such as specifying the sound effects
        or the GPIO channels.
    app : str
        Name of the application to use for opening the config file, e.g. 
        `TextEdit` (the default value is None which implies that the default
        application will be used to open the config file).

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
    args : argparse.ArgumentParser
        Argument parser.

    """
    # Help message that is used in various arguments
    common_help = '''Provide 'log' (without the quotes) for the logging config 
        file or 'main' (without the quotes) for the main config file.'''
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        # prog=os.path.basename(__file__),
        description='''\
Activate Darth Vader by turning on LEDs on his suit and lightsaber, and by 
pressing buttons to produce sound effects.\n
IMPORTANT: these are only some of the most important options. Open the main 
config file to have access to the complete list of options, i.e. 
%(prog)s -e main''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # ===============
    # General options
    # ===============
    parser.add_argument("--version", action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Enable quiet mode, i.e. nothing will be printed.")
    parser.add_argument("-s", "--simulation", action="store_true",
                        help="Enable simulation mode, i.e. SimulRPi.GPIO wil be "
                             "used for simulating RPi.GPIO.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print various debugging information, e.g. print "
                             "traceback when there is an exception.")
    # Group arguments that are closely related
    # ===========
    # Edit config
    # ===========
    edit_group = parser.add_argument_group('Edit a configuration file')
    edit_group.add_argument(
        "-e", "--edit", choices=["log", "main"],
        help="Edit a configuration file. {}".format(common_help))
    edit_group.add_argument(
        "-a", "--app-name", default=None, dest="app",
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
        "-r", "--reset", choices=["log", "main"],
        help='''Reset a configuration file with factory default values. 
            {}'''.format(common_help))
    reset_group.add_argument(
        "-u", "--undo", choices=["log", "main"],
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
    global logger, GPIO
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
            keys = ['handlers', 'loggers']
            for k in keys:
                for name, val in logging_cfg_dict[k].items():
                    val['level'] = "DEBUG"
            logger.info("Verbose option enabled")
        logging.config.dictConfig(logging_cfg_dict)
        logger_name = "{}.{}".format(
            package_name,
            os.path.splitext(__file__)[0])
        logger = logging.getLogger(logger_name)
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
    retcode = 1
    try:
        if args.edit:
            retcode = edit_config(args.edit, args.app)
            """
            elif args.reset:
                retcode = reset_config(args.reset)
            elif args.undo:
                retcode = undo_config(args.undo)
            """
        else:
            if main_cfg_dict['simulation']:
                import SimulRPi.GPIO
                GPIO = SimulRPi.GPIO
                GPIO.setkeymap(main_cfg_dict['key_to_channel_mapping'])
                if main_cfg_dict['quiet']:
                    GPIO.disableprinting()
                logger.info("Simulation mode enabled")
            else:
                import RPi.GPIO
                GPIO = RPi.GPIO
            # TODO: works on UNIX shell only, not Windows
            # ref.: https://bit.ly/3f3A7dc
            os.system("tput civis")
            retcode = activate_dv(main_cfg_dict)
    # except (AssertionError, AttributeError, KeyError, ImportError, OSError) as e:
    except Exception as e:
        # TODO: explain this line
        # traceback.print_exc()
        if args.verbose:
            logger.exception(e)
        else:
            logger.error(e.__repr__())
    finally:
        # TODO: works on UNIX shell only, not Windows
        os.system("tput cnorm")
        if main_cfg_dict['quiet']:
            print()
        return retcode


if __name__ == '__main__':
    retcode = main()
    msg = "Program exited with {}".format(retcode)
    if retcode == 1:
        logger.error(msg)
    else:
        logger.debug(msg)
