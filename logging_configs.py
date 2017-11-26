import collections
import logging
import logging.config
from copy import deepcopy

_default = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s; %(name)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'graph_printing': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'simulation': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'visualization': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'benchmark_results': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'algo_vis_last': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'algo_populations': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'per_iter_stats': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
        'new_solution': {
            'handlers': ['default'],
            'level': 'WARN',
            'propagate': True
        },
    }
}


def parse_str_config(config_string):
    """

    :param config_string: example - graph_printing=info,benchmark_results=info
    :return:
    """
    config_dict = {
        "loggers": dict()
    }

    if config_string:
        for logger_conf in config_string.split(","):
            if "=" in logger_conf:
                raw_logger_name, raw_level = logger_conf.split("=")
            else:
                raw_logger_name = logger_conf
                raw_level = "INFO"
            logger_name = raw_logger_name.lower()
            level = logging.getLevelName(raw_level.upper())
            config_dict["loggers"][logger_name] = {"level": level}

    return config_dict


def build_config(overrides, overrides_only_loggers=True):
    new_config = deepcopy(_default)
    if overrides_only_loggers:
        merge_target = new_config["loggers"]
    else:
        merge_target = new_config
    dict_merge(merge_target, overrides)
    return new_config


def configure_logging(conf):
    if isinstance(conf, basestring):
        config_dict = build_config(parse_str_config(conf), False)
    else:
        config_dict = conf
    logging.config.dictConfig(config_dict)


def dict_merge(dct, merge_dct):
    """
    From https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

    Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
            and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
