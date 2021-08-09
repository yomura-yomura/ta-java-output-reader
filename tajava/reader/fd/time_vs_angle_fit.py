from . import _util
import numpy as np
import scipy.constants
import pathlib


__all__ = ["load", "timing_fit"]


def _parse_line(line):
    buffer = line.split()
    return *_util.parse_event_info(*buffer[:6]), *buffer[6:]


def load(path):
    path = pathlib.Path(path)
    if path.is_dir():
        path /= "time_vs_angle_fit.dat"
    elif not path.exists():
        raise FileNotFoundError(path)

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("tau0", "f4"),
                ("Rp", "f4"),
                ("psi", "f4")
            ]
        )


refractive_index_of_air = 1.000292  # 0℃、1気圧
air_light_speed = scipy.constants.c / refractive_index_of_air * 100 / 1e9  # cm/ns


def timing_fit(χ, τ0, Rp, ψ):
    return τ0 + Rp / air_light_speed * np.tan((np.pi - ψ - χ) * 0.5)
