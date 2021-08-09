import pathlib

from . import _util
import numpy as np


__all__ = ["load"]


def _parse_line(line):
    buffer = line.split()
    return *_util.parse_event_info(*buffer[:6]), *buffer[6:]


def load(path):
    path = pathlib.Path(path)
    if path.is_dir():
        path /= "geom_polar_track_recon4tale.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("azimuth", "f8"),
                ("zenith", "f8")
            ]
        )
