#!/usr/bin/env python
"""Script to turn on LEDs and play sound effects on a Raspberry Pi (RPi).

The LEDs illuminate a Darth Vader action figure's lightsaber and the three
slots in the chest control box. 3 push buttons control the following sounds
and LEDs:

1. Some of his famous quotes
2. The Imperial march theme song
3. The lightsaber drawing, hum and retraction sounds
4. The lightsaber illumination (3 LEDs)

His iconic breathing sound plays in the background indefinitely almost as soon
as the RPi is run with the script.

The script allows you also to edit the `main config file`_ to setup among other
things the RPi's GPIO pins connected to LEDs and push buttons.

By default the module `RPi.GPIO`_ is used, but if the simulation option (`-s`)
is used with the script :mod:`start_dv`, then the module `SimulRPi.GPIO`_ will
be used instead which simulates `RPi.GPIO`_ for those that don't have an RPi to
test on.

.. _usage-start-dv-label:

Usage
-----

.. highlight:: console

Once the package ``darth_vader_rpi`` is `installed`_, you should have access to
the script :mod:`start_dv`:

    ``start_dv [-h] [--version] [-q] [-s] [-v] [-e {log,main}] [-a APP]``

Run the script on the **RPi** with `default values`_ for the  GPIO channels and
other settings::

    $ start_dv

Run the script on your **computer** using :mod:`SimulRPi.GPIO` which simulates
``RPi.GPIO``::

    $ start_dv -s

Edit the main config file with *TextEdit* (e.g. on macOS)::

    $ start_dv -e main -a TextEdit

Edit the logging config file with a default application (e.g. atom)::

    $ start_dv -e log

.. highlight:: python

Notes
-----
More information is available at:

- `Darth-Vader-RPi GitHub`_
- `SimulRPi GitHub`_

.. note::

    In :mod:`darth_vader` and :mod:`ledutils`, the default value for ``GPIO``
    is :obj:`None` and will be eventually set to one of the two modules
    (`RPi.GPIO`_ or `SimulRPi.GPIO`_) depending on the user's settings.

    `RPi.GPIO`_ provides a class to control the GPIO pins on a Raspberry Pi.

    If the `simulation` option (`-s`) is used with the script :mod:`start_dv`,
    the `SimulRPi.GPIO`_ module will be used instead.

.. URLs

.. default_main_cfg
.. _default values: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json
.. _logging config file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_logging_cfg.json
.. _main config file: https://github.com/raul23/Darth-Vader-RPi/blob/master/darth_vader_rpi/configs/default_main_cfg.json

.. external links
.. _Darth-Vader-RPi GitHub: https://github.com/raul23/Darth-Vader-RPi
.. _RPi.GPIO: https://pypi.org/project/RPi.GPIO/
.. _SimulRPi GitHub: https://github.com/raul23/SimulRPi
.. _SimulRPi.GPIO: https://pypi.org/project/SimulRPi/

.. internal links
.. _installed: README_docs.html#installation-instructions

"""
import argparse
import logging.config
import os
import platform
import shutil
from collections import namedtuple
from logging import NullHandler

from dv_sounds.utils import get_dirpath, get_filepath
from darth_vader_rpi import (__name__ as package_name,
                             __path__ as package_path,
                             __version__ as package_version)
from darth_vader_rpi.darth_vader import DarthVader
from darth_vader_rpi.utils import (add_spaces_to_msg, dumps_json,
                                   get_cfg_filepath, load_json,
                                   override_config_with_args, run_cmd)

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

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


def _check_user_cfg_dict(cfg_type, user_cfg_dict):
    """TODO

    Parameters
    ----------
    cfg_type
    user_cfg_dict

    """
    retval = namedtuple("retval", "keys_not_found user_cfg_filepath")
    retval.keys_not_found = []
    user_cfg_filepath = get_cfg_filepath(cfg_type)
    retval.user_cfg_filepath = user_cfg_filepath
    default_cfg_filepath = get_cfg_filepath("default_{}".format(cfg_type))
    default_cfg_dict = load_json(default_cfg_filepath)
    default_keys = set(default_cfg_dict.keys())
    user_keys = set(user_cfg_dict.keys())
    diff_keys = default_keys - user_keys
    for k in diff_keys:
        retval.keys_not_found.append(k)
        user_cfg_dict.setdefault(k, default_cfg_dict[k])
    if diff_keys:
        dumps_json(filepath=user_cfg_filepath, data=user_cfg_dict, indent=2)
    return retval


def _check_sound_files(main_cfg):
    """TODO

    Parameters
    ----------
    main_cfg

    Raises
    ------
    FileNotFoundError

    """
    logger.debug("Checking sound files...")
    default_directory = False
    if main_cfg['sounds_directory']:
        logger.debug("sounds_directory: {}".format(
            main_cfg['sounds_directory']))
    else:
        default_directory = True
        logger.info("No sounds_directory defined in config file")
        dirpath = get_dirpath()
        logger.info("Setting sounds_directory with default location: "
                    "{}".format(dirpath))
        orig_main_cfg = _get_cfg_dict('main')
        orig_main_cfg['sounds_directory'] = dirpath
        main_cfg['sounds_directory'] = dirpath
        dumps_json(get_cfg_filepath('main'), orig_main_cfg, indent=2)
    sound_types = ['quotes', 'songs', 'sound_effects']
    for sound_type in sound_types:
        for sound in main_cfg[sound_type]:
            filename = sound['filename']
            if default_directory:
                filepath = get_filepath(filename)
            else:
                filepath = os.path.join(main_cfg['sounds_directory'], filename)
            if os.path.exists(filepath):
                logger.debug("File checked: {}".format(filepath))
            else:
                raise FileNotFoundError("No such file: {}".format(filepath))


def _get_cfg_dict(cfg_type):
    """TODO

    Parameters
    ----------
    cfg_type

    Returns
    -------

    """
    test_cfg = {'main': _TEST_MAIN_CFG,
                'log': _TEST_LOGGING_CFG}
    cfg_dict = test_cfg[cfg_type]
    if cfg_dict is None:
        cfg_filepath = get_cfg_filepath(cfg_type)
        try:
            cfg_dict = load_json(cfg_filepath)
        except FileNotFoundError:
            # TODO: IMPORTANT add logging
            # Config file not found
            # Copy it from the default one
            # TODO: IMPORTANT destination with default?
            default_cfg_type = "default_{}".format(cfg_type)
            src = get_cfg_filepath(default_cfg_type)
            shutil.copy(src, cfg_filepath)
            cfg_dict = load_json(cfg_filepath)
    if 'sounds_directory' in cfg_dict:
        # Only for main config file
        cfg_dict['sounds_directory'] = os.path.expanduser(
            cfg_dict['sounds_directory'])
    return cfg_dict


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
    app : str, optional
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
        # a command along with the file path, e.g. ``$ atom {filepath}``.
        # However, this case might not work if the user provided an app name
        # that doesn't refer to an executable, e.g. ``$ TextEdit {filepath}``
        # won't work. The failed case is further processed in the except block.
        result = run_cmd(cmd.format(filepath=filepath))
        retcode = result.returncode
    except FileNotFoundError:
        # This error happens if the name of the app can't be called as an
        # executable in the terminal
        # e.g. `TextEdit` can't be run in the terminal but `atom` can since the
        # latter refers to an executable.
        # To open `TextEdit` from the terminal, the command ``open -a TextEdit``
        # must be used on macOS.
        # TODO: IMPORTANT add the open commands for the other OSes
        specific_cmd_dict = {'Darwin': 'open -a {app}'.format(app=app)}
        # Get the command to open the file with the user-specified app
        cmd = specific_cmd_dict.get(platform.system(), app) + " " + filepath
        # TODO: explain DEVNULL, suppress stderr since we will display the error
        # TODO: IMPORTANT you might get a FileNotFoundError again?
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

    - activate a Darth Vader figurine (turn on LEDs and play sound effects)
    - edit a configuration file

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
                        version='%(prog)s {}'.format(package_version))
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

    - activate a Darth Vader figurine (turn on LEDs and play sound effects)
    - edit a configuration file

    Raises
    ------
    ValueError
        Raised if an invalid configuration name is given to the
        command-line argument `edit`.

    Notes
    -----
    Only one action at a time can be performed.

    """
    global logger, GPIO
    # =====================
    # Default logging setup
    # =====================
    # Setup the default logger (whose name is __main__ since this file is run
    # as a script) which will be used for printing to the console before all
    # loggers defined in the JSON file will be configured. The printing with
    # this default logger will only be done in the cases that the user allows
    # it, e.g. the verbose option is enabled.
    # IMPORTANT: the config options need to be read before using any logger
    # TODO: default logger not used
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # ============================
    # Parse command-line arguments
    # ============================
    parser = setup_argparser()
    args = parser.parse_args()
    # Get main config dict and check if keys missing
    main_cfg_dict = _get_cfg_dict('main')
    check_cfg_retval = _check_user_cfg_dict('main', main_cfg_dict)
    # Override logging configuration with command-line arguments
    override_retval = override_config_with_args(main_cfg_dict, parser)

    # ==============================
    # Logging setup from config file
    # ==============================
    # NOTE: if quiet and verbose are both activated, only quiet will have an effect
    if main_cfg_dict['quiet']:
        # TODO: disable logging completely? even error messages?
        logger.disabled = True
    else:
        # Setup logger
        logging_cfg_dict = _get_cfg_dict('log')
        # NOTE: returned value not used
        _check_user_cfg_dict('log', logging_cfg_dict)
        if main_cfg_dict['verbose']:
            keys = ['handlers', 'loggers']
            for k in keys:
                for name, val in logging_cfg_dict[k].items():
                    val['level'] = "DEBUG"
        logging.config.dictConfig(logging_cfg_dict)
        if __name__ == '__main__':
            logger_name = "{}.{}".format(
                package_name,
                os.path.splitext(__file__)[0])
        else:
            logger_name = __name__
        logger = logging.getLogger(logger_name)

    # ==================================================
    # Start logging and process previous returned values
    # ==================================================
    logger.info("Running {} v{}".format(package_name, package_version))
    logger.debug("Package path: {}".format(package_path[0]))
    logger.info("Verbose option {}".format(
        "enabled" if main_cfg_dict['verbose'] else "disabled"))
    # Process first returned values: checking config file
    if check_cfg_retval.keys_not_found:
        logger.debug("checked user configuration file '{}'...".format(
            os.path.basename(check_cfg_retval.user_cfg_filepath)))
        for k in check_cfg_retval.keys_not_found:
            logger.warning("Key '{}' not found. Added it in the configuration "
                           "dict with default values.".format(k))
        logger.info("Saved updated configuration dict to file: {}".format(
            check_cfg_retval.user_cfg_filepath))
    # Process second returned values: overridden config options
    if override_retval.config_opts_overridden:
        msg = "Config options overridden by command-line arguments:\n"
        config_opts_overridden = override_retval.config_opts_overridden
        nb_items = len(config_opts_overridden)
        for i, (cfg_name, old_v, new_v) in enumerate(config_opts_overridden):
            msg += "\t {}: {} --> {}".format(cfg_name, old_v, new_v)
            if i + 1 < nb_items:
                msg += "\n"
        logger.debug(msg)
    # Process third returned values: arguments not found in cfg file
    if override_retval.args_not_found:
        msg = "Command-line arguments not found in JSON config file: " \
              "{}".format(override_retval.args_not_found)
        logger.debug(msg)

    # =======
    # Actions
    # =======
    retcode = 0
    # TODO: enlarge try? even if logger not setup completely
    try:
        _check_sound_files(main_cfg_dict)
        if args.app and not args.edit:
            raise RuntimeError("You need to also specify the edit argument "
                               "'-e'")
        elif args.edit:
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
        else:
            if main_cfg_dict['simulation']:
                import SimulRPi.GPIO as GPIO
                GPIO.setchannels(main_cfg_dict['gpio_channels'])
                GPIO.setdefaultsymbols(main_cfg_dict['default_led_symbols'])
                GPIO.setprinting(not main_cfg_dict['quiet'])
                logger.debug("Simulation mode enabled")
            else:
                import RPi.GPIO as GPIO
            # TODO: find another way
            from darth_vader_rpi import darth_vader
            darth_vader.GPIO = GPIO
            from darth_vader_rpi import ledutils
            ledutils.GPIO = GPIO
            # TODO: works on UNIX shell only, not Windows
            # ref.: https://bit.ly/3f3A7dc
            # os.system("tput civis")
            dv = DarthVader(main_cfg_dict)
            retcode = dv.activate()
    except Exception as e:
        # TODO: explain this line
        # traceback.print_exc()
        if args.verbose:
            logger.exception(e)
        else:
            # logger.error(e.__repr__())
            # TODO: add next line in a utility function
            # TODO: add spaces?
            err_msg = "{}: {}".format(str(e.__class__).split("'")[1], e)
            logger.error(err_msg)
        retcode = 1
    except KeyboardInterrupt:
        # Might happen if error in Manager.{on_press(), on_release()} and then
        # ctrl+c. Not enough time given to stop all threads
        # TODO: dv.check_cleanup()
        # TODO: GPIO.manager.check_cleanup()
        if dv.th_slot_leds and dv.th_slot_leds.is_alive():
            dv.th_slot_leds.join()
            logger.warning("Abrupt exit: the thread '{}' was not cleanly "
                           "stopped".format(dv.th_slot_leds.name))
            logger.debug(add_spaces_to_msg("Thread stopped: {}".format(
                dv.th_slot_leds.name)))
            retcode = 1
        if hasattr(GPIO, 'manager'):
            # Simulation only
            if (GPIO.manager.th_listener and
                GPIO.manager.th_listener.is_alive()) or \
                    GPIO.manager.th_display_leds.is_alive():
                logger.warning("Abrupt exit: GPIO threads were not cleanly "
                               "stopped")
                GPIO.cleanup()
                retcode = 1
        if retcode == 1:
            logger.warning("CAUSE: threads were not given enough time to "
                           "be stopped at the moment of the raised exception. "
                           "However, all threads are now stopped.")

    finally:
        if main_cfg_dict['quiet']:
            print()
        return retcode


if __name__ == '__main__':
    retcode = main()
    msg = "Program exited with {}".format(retcode)
    if retcode == 1:
        logger.error(add_spaces_to_msg(msg))
    else:
        logger.info(add_spaces_to_msg(msg))
