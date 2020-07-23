import codecs
import json

from collections import namedtuple


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


def override_config_with_args(config, args):
    retval = namedtuple("retval", "args_not_found config_opts_overidden")
    retval.args_not_found = []
    retval.config_opts_overidden = []
    for k, new_v in args.__dict__.items():
        old_v = config.get(k)
        if old_v is not None:
            if new_v != old_v:
                config[k] = new_v
                retval.config_opts_overidden.append((k, old_v, new_v))
        else:
            retval.args_not_found.append(k)
    return retval
