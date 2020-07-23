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
