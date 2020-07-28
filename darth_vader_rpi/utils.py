"""Collection of utilities specifically for the Darth-Vader-RPi project.

.. _default logging configuration file: https://bit.ly/2D6exaD
.. _default main configuration file: https://bit.ly/39x8o3e

"""
import os
from collections import namedtuple

from darth_vader_rpi import configs


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
    """Get the path to the directory containing the config files.

    Returns
    -------
    dirpath : str
        The path to the directory containing the config files.

    See Also
    --------
    get_cfg_filepath : Get the path to a config file.

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
