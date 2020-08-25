"""Collection of utilities specifically for the *Darth-Vader-RPi* project.

.. _default logging configuration file: https://bit.ly/2D6exaD
.. _default main configuration file: https://bit.ly/39x8o3e

"""
import codecs
import json
import os
import shlex
import subprocess
from collections import namedtuple

from darth_vader_rpi import configs


# TODO: explain
_CFG_EXT = "json"
_LOG_CFG_FILENAME = 'logging_cfg'
_MAIN_CFG_FILENAME = 'main_cfg'
_CFG_FILENAMES = namedtuple("cfg_filenames", "user_cfg default_cfg")


def _add_cfg_filenames():
    """TODO
    """
    _CFG_FILENAMES.user_cfg = {
        'log': '{}.'.format(_LOG_CFG_FILENAME) + _CFG_EXT,
        'main': '{}.'.format(_MAIN_CFG_FILENAME) + _CFG_EXT}
    _CFG_FILENAMES.default_cfg = dict(
        [("default_" + k, "default_" + v)
         for k, v in _CFG_FILENAMES.user_cfg.items()])


_add_cfg_filenames()


def get_cfg_dirpath():
    """Get the path to the directory containing the config files.

    Returns
    -------
    dirpath : str
        The path to the directory containing the config files.

    """
    return configs.__path__[0]


def get_cfg_filepath(file_type):
    """Get the path to a config file used by the :mod:`start_dv` script.

    The config file can either be the:

    - **default_log**: refers to the `default logging configuration file`_ used
      to setup the logging for all custom modules.
    - **default_main**: refers to the `default main configuration file`_ used to
      setup the :mod:`start_dv` script.
    - **log**: refers to the user-defined logging configuration file which is
      used to setup the logging for all custom modules.
    - **main**: refers to the user-defined main configuration file used to
      setup the :mod:`start_dv` script.

    Parameters
    ----------
    file_type : str, {'default_log', 'default_main', 'log', 'main'}
        The type of config file for which we want the path.

    Returns
    -------
    filepath : str
        The path to the config file.

    Raises
    ------
    AssertionError
        Raised if the wrong type of config file is given to the function. Only
        {'default_log', 'default_main', 'log', 'main'} are accepted for
        `file_type`.

    """
    # TODO: explain
    valid_file_types = list(_CFG_FILENAMES.user_cfg.keys()) \
        + list(_CFG_FILENAMES.default_cfg.keys())
    assert file_type in valid_file_types, \
        "Wrong type of config file: '{}' (choose from {})".format(
            file_type, ", ".join(valid_file_types))
    if file_type.startswith('default'):
        filename = _CFG_FILENAMES.default_cfg[file_type]
    else:
        filename = _CFG_FILENAMES.user_cfg[file_type]
    return os.path.join(get_cfg_dirpath(), filename)


def load_json(filepath, encoding='utf8'):
    """Load JSON data from a file on disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file which will be read.
    encoding : str, optional
        Encoding to be used for opening the JSON file in read mode (the default
        value is 'utf8').

    Returns
    -------
    data
        Data loaded from the JSON file.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.

    """
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            data = json.load(f)
    except OSError:
        raise
    else:
        return data


def override_config_with_args(config, parser):
    """Override a config dictionary with arguments from the command-line.

    Parameters
    ----------
    config : dict

    parser : argparse.ArgumentParser
        Argument parser.

    Returns
    -------
    retval : :obj:`collections.namedtuple`
        Contains two lists:

        1. `args_not_found`: stores command-line arguments not found in the
        JSON file

        2. `config_opts_overidden`: stores config options overriden by
        command-line arguments as a three-tuple (option name, old value,
        new value)

    """
    args = parser.parse_args().__dict__
    parser_actions = parser.__dict__['_actions']
    retval = namedtuple("retval", "args_not_found config_opts_overidden")
    retval.args_not_found = []
    retval.config_opts_overidden = []
    for action in parser_actions:
        opt_name = action.dest
        old_val = config.get(opt_name)
        if old_val is None:
            retval.args_not_found.append(opt_name)
        else:
            new_val = args.get(opt_name)
            if new_val is None:
                continue
            if new_val != action.default and new_val != old_val:
                config[opt_name] = new_val
                retval.config_opts_overidden.append((opt_name, old_val, new_val))
    return retval


# NOTE: taken from pyutils.genutils
def run_cmd(cmd, stderr=subprocess.STDOUT):
    """Run a command with arguments.

    The command is given as a string but the function will split it in order to
    get a list having the name of the command and its arguments as items.

    Parameters
    ----------
    cmd : str
        Command to be executed, e.g. ::

            open -a TextEdit text.txt
    stderr

    Returns
    -------
    retcode: int
        Return code which is 0 if the command was successfully completed.
        Otherwise, the return code is non-zero.

    Raises
    ------
    FileNotFoundError
        Raised if the command ``cmd`` is not recognized, e.g.
        ``$ TextEdit {filepath}`` since `TextEdit` is not an executable.

    """
    try:
        # `check_call()` takes as input a list. Thus, the string command must
        # be split to get the command name and its arguments as items of a list.
        # NOTE: To suppress stdout or stderr, supply a value of DEVNULL
        #       Ref.: https://bit.ly/35NqiN0
        """
        retcode = subprocess.check_call(shlex.split(cmd), stderr=stderr)
        """
        result = subprocess.run(shlex.split(cmd), capture_output=True)
    except subprocess.CalledProcessError as e:
        return e
    except FileNotFoundError:
        raise
    else:
        return result
