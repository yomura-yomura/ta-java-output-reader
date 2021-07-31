# import pandas as pd
from . import _util
import numpy as np


__all__ = ["load"]


def load(path):
    def _parse_line(line):
        buffer = line.split()
        return *_util.parse_event_info(*buffer[:6]), *buffer[6:-3], tuple(buffer[-3:])

    with open(path) as f:
        return np.fromiter(
            map(_parse_line, f),
            dtype=[
                *_util.event_info_dtype_descr,
                ("pmt_id", "i8"),
                ("chi_angle", "f8"),
                ("nanosecond", "f8"),
                ("error_nanosecond", "f8"),
                ("direction", [
                    ("x", "f8"),
                    ("y", "f8"),
                    ("z", "f8")
                ])
            ]
        )

    # df = pd.read_csv(path, delim_whitespace=True, header=None, parse_dates=[[4, 5]])
    # df = df.rename(
    #     columns={
    #         0: "detector_type", 1: "fd_type", 2: "part", 3: "event_number",
    #         # 4: "date", 5: "time",
    #         "4_5": "event_datetime",
    #         6: "pmt_id", 7: "chi_angle", 8: "nanosecond", 9: "error_nanosecond",
    #         10: "dir_x", 11: "dir_y", 12: "dir_z"
    #     }
    # )
    #
    # df = df.drop(columns=["detector_type", "fd_type"])
    # df = df.set_index(["event_datetime", "part", "event_number"])
    # return df
