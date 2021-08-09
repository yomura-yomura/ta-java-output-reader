from . import _util
import numpy as np
import pathlib

__all__ = ["load"]


def _parse_line(line):
    buffer = line.split()
    return *_util.parse_event_info(*buffer[:6]), *buffer[6:]


def load(path):
    path = pathlib.Path(path)
    if path.is_dir():
        path /= "time_vs_angle.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("alpha", "f4"),
                ("t", "f4"),
                ("t_err", "f4"),
                ("station_id", "i4")
            ]
        )
