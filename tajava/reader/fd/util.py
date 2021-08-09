from ._util import event_info_dtype_descr
import numpy as np


def get_matched(data, part, event_number, date):
    matched_data = data[
        (data["part"] == part) &
        (data["event_number"] == event_number) &
        (data["t0"].astype("M8[D]") == date)
    ]
    event_info_names = [n for n, *_ in event_info_dtype_descr]
    assert np.unique(matched_data[event_info_names]).size == 1
    return matched_data
