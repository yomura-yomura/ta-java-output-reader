from . import _util
import numpy as np
import scipy.constants
import pathlib


__all__ = ["load"]


def _parse_line(line):
    buffer = line.split()
    return int(buffer[0]), *_util.parse_event_info(*buffer[1:7]), *buffer[7:]


def load(path):
    path = pathlib.Path(path)
    if path.is_dir():
        path /= "hybridrecon.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                ("is_true", "bool"),
                *_util.event_info_dtype_descr,
                ("x", "f8"),
                ("y", "f8"),
                ("azimuth", "f8")
            ]
        )
