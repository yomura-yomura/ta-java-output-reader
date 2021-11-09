"""
see TAFDReconstructor._printResultsSimple2
"""

import numpy as np
from . import _util


__all__ = ["load"]


def _parse_block(block: str):
    lines = block.splitlines()
    assert lines[1].startswith("Sim Geom ")
    split_line1 = lines[1].split()
    return (
        _util.parse_event_info(*lines[0].split()),
        (*split_line1[3:-3], tuple(split_line1[-3:]))
    )


def load(path):
    with open(path, "r") as f:
        blocks = [stripped_block for block in f.read().split("\n\n") if (stripped_block := block.strip())]

    return np.array(
        list(map(_parse_block, blocks)),
        dtype=[
            ("event_info", _util.event_info_dtype_descr),
            ("geom", [("zenith", "f4"), ("azimuth", "f4"), ("core_position", ("f4", 3))])
         ]
    )
