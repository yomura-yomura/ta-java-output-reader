__all__ = ["event_info_dtype_descr", "parse_event_info"]


event_info_dtype_descr = [
    ("detector_type", "i2"),
    ("fd_type", "i2"),
    ("part", "i4"),
    ("event_number", "i4"),
    ("t0", "M8[ns]")
]


def parse_event_info(detector_type, fd_type, part, event_number, date, time):
    """
        ("detector_type", "i2"),
        ("fd_type", "i2"),
        ("part", "i4"),
        ("event_number", "i4"),
        ("t0", "M8[ns]"),
    """
    return detector_type, fd_type, part, event_number, "{}T{}".format(date.replace("/", "-"), time)
