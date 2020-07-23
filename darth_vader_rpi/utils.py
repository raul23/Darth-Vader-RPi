import codecs
import json
import os
import shlex
import subprocess

from collections import namedtuple

import configs


_CFG_EXT = "json"
_LOG_CFG_FILENAME = 'logging_cfg'
_MAIN_CFG_FILENAME = 'main_cfg'
_cfg_filenames = namedtuple("cfg_filenames", "user_cfg default_cfg")


def _add_cfg_filenames():
    """TODO
    """
    _cfg_filenames.user_cfg = {
        'log': '{}.'.format(_LOG_CFG_FILENAME) + _CFG_EXT,
        'main': '{}.'.format(_MAIN_CFG_FILENAME) + _CFG_EXT}
    _cfg_filenames.default_cfg = dict(
        [("default_" + k, "default_" + v)
         for k, v in _cfg_filenames.user_cfg.items()])


_add_cfg_filenames()


def get_cfg_dirpath():
    """TODO

    Returns
    -------

    """
    return configs.__path__[0]


def get_cfg_filepath(file_type):
    """Return the path to a config file used by :mod:`lyrics_scraping`.

    The config file can either be the:

    - **default_log**: refers to the `default logging configuration file`_ used
      to setup the logging for all custom modules.
    - **default_main**: refers to the `default main configuration file`_ used to
      setup a lyrics scraper.
    - **log**: refers to the `user-defined logging configuration file`_ which is
      used to setup the logging for all custom modules.
    - **main**: refers to the `user-defined main configuration file`_ used to
      setup a lyrics scraper.

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
    valid_file_types = list(_cfg_filenames.user_cfg.keys()) \
        + list(_cfg_filenames.default_cfg.keys())
    assert file_type in valid_file_types, \
        "Wrong type of config file: '{}' (choose from {})".format(
            file_type, ", ".join(valid_file_types))
    if file_type.startswith('default'):
        filename = _cfg_filenames.default_cfg[file_type]
    else:
        filename = _cfg_filenames.user_cfg[file_type]
    return os.path.join(get_cfg_dirpath(), filename)


# TODO: use load_json() from pyutils
def load_json(filepath, encoding='utf8'):
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            data = json.load(f)
    except OSError:
        raise
    else:
        return data


def msg_with_spaces(msg, nb_spaces=20):
    return "{}{}".format(msg, " " * nb_spaces)


def override_config_with_args(config, parser):
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


# TODO: use run_cmd() from pyutils
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
        TODO command not recognized, e.g. `$ TextEdit {filepath}`

    Examples
    --------
    TODO

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
