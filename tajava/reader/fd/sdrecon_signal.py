from . import _util
import numpy as np
import scipy.constants
import pathlib


__all__ = ["load"]


def _parse_line(line):
    buffer = line.split()
    return *_util.parse_event_info(*buffer[:6]), *buffer[6:]


def load(path):
    path = pathlib.Path(path)
    if path.is_dir():
        path /= "sdrecon_signal.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("lid", "f4"),
                ("x", "f8"),
                ("y", "f8"),
                ("z", "f8"),
                ("t", "f8"),
                ("Q", "f8")
            ]
        )
