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
        path /= "sdrecon_lateral_density.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("lid", "f4"),
                ("r", "f4"),
                ("Q", "f4")
            ]
        )
