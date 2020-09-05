"""Collection of utilities specifically for the *Darth-Vader-RPi* project.

.. _default logging configuration file: https://bit.ly/2D6exaD
.. _default main configuration file: https://bit.ly/39x8o3e

"""
import codecs
import json
import os
import shlex
import subprocess
import sys
from collections import namedtuple, OrderedDict
# from subprocess import PIPE

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

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


# TODO: clear buffer?
def _add_spaces_to_msg(msg, nb_spaces=60):
    """TODO

    Parameters
    ----------
    msg
    nb_spaces

    Returns
    -------

    """
    return "{}{}".format(msg, " " * nb_spaces)


# TODO: fix in genutils new changes
def dumps_json(filepath, data, encoding='utf8', ensure_ascii=False,
               indent=None, sort_keys=False):
    """Write data to a JSON file.

    The data is first serialized to a JSON formatted string and then saved
    to disk.

    Parameters
    ----------
    filepath : str
        Path to the JSON file where the data will be saved.
    data
        Data to be written to the JSON file.
    encoding : str, optional
        Encoding to be used for opening the JSON file in write mode (the
        default value is 'utf8').
    ensure_ascii : bool, optional
        If ``ensure_ascii`` is False, then the return value can contain
        non-ASCII characters if they appear in strings contained in ``data``.
        Otherwise, all such characters are escaped in JSON strings. See the
        :meth:`json.dumps` docstring description (the default value is False).
    indent : int or None, optional
        If ``indent`` is a non-negative integer, then JSON array elements and
        object members will be pretty-printed with that indent level. An indent
        level of 0 will only insert newlines. :obj:`None` is the most compact
        representation. See the :meth:`json.dumps` docstring description. (the
        default value is :obj:`None`).
    sort_keys : bool, optional
        If `sort_keys` is true, then the output of dictionaries will be sorted
        by key. See the :meth:`json.dumps` docstring description. (the default
        value is False).

    Raises
    ------
    OSError
        Raised if any I/O related occurs while writing the data to disk, e.g.
        the file doesn't exist.

    """
    try:
        with codecs.open(filepath, 'w', encoding) as f:
            f.write(json.dumps(data,
                               ensure_ascii=ensure_ascii,
                               indent=indent,
                               sort_keys=sort_keys))
    except OSError:
        raise


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

    TODO: specify preserve order if py36 and less

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
            if sys.version_info.major == 3 and sys.version_info.minor <= 6:
                data = json.load(f, object_pairs_hook=OrderedDict)
            else:
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
        TODO

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
        # TODO: remove following comments
        # `check_call()` takes as input a list. Thus, the string command must
        # be split to get the command name and its arguments as items of a list.
        # NOTE: To suppress stdout or stderr, supply a value of DEVNULL
        # Ref.: https://bit.ly/35NqiN0
        """
        retcode = subprocess.check_call(shlex.split(cmd), stderr=stderr)
        """
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # TODO: PIPE not working as arguments
            # Ref.: https://stackoverflow.com/a/53209196
            #       https://bit.ly/3lvdGlG
            result = subprocess.run(shlex.split(cmd))
        else:
            result = subprocess.run(shlex.split(cmd), capture_output=True)
        """
        except subprocess.CalledProcessError:
            return e
        """
    except FileNotFoundError:
        raise
    else:
        return result


class _SoundWrapper:
    """Class that wraps around :class:`pygame.mixer.Channel` and
    :class:`pygame.mixer.Sound`.

    The :meth:`__init__` method takes care of automatically loading the sound
    file. The sound file can then be played or stopped from the specified
    channel `channel_id` with the :meth:`play` or :meth:`stop` method,
    respectively.

    Parameters
    ----------
    sound_id : str
        A unique identifier.
    sound_name : str
        Name of the sound file that will be displayed in the terminal.
    sound_filepath : str
        Path to the sound file.
    channel_id : int
        Channel id associated with an instance of
        :class:`pygame.mixer.Channel` for controlling playback. It must take an
        :obj:`int` value starting from 0.
    mute : bool, optional
        If set to `True`, the sound will not be played. The default value is
        `False`.


    .. note::

        It is a wrapper with a very minimal interface to
        :class:`pygame.mixer.Channel` where only two methods :meth:`play` and
        :meth:`stop` are provided for the sake of the project.

    """

    def __init__(self, sound_id, sound_name, sound_filepath, channel_id,
                 mute=False):
        self.sound_id = sound_id
        self.sound_name = sound_name
        self.sound_filepath = sound_filepath
        self.channel_id = channel_id
        self.mute = mute
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
            :meth:`stop` to stop it).

            **Reference:** :meth:`pygame.mixer.Sound.play`

        """
        self._channel.play(self._pygame_sound, loops)

    def stop(self):
        """Stop playback on the specified channel `channel_id`.
        """
        self._channel.stop()
