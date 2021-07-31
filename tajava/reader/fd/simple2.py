"""
see TAFDReconstructor._printResultsSimple2
"""

import numpy as np
from . import _util
import re
import itertools


__all__ = ["load"]

pattern = re.compile(r"""(\d+) (\d+) (\d+) (\d+) (\d+/\d+/\d+) (\d+:\d+:\d+\.\d+)
""")


def load(path):
    with open(path, "r") as f:
        data = pattern.findall(f.read())

    event_info = np.array(
        list(itertools.starmap(_util.parse_event_info, data)), dtype=_util.event_info_dtype_descr
    )
    return event_info
