"""
see TAFDReconstructor._printResultsSimple3
"""
import numpy as np
import copy
from . import _util


def i_to_f(d):
    if isinstance(d, list):
        return [i_to_f(e) for e in d]
    elif isinstance(d, tuple):
        if isinstance(d[1], tuple):
            return d[0], (i_to_f(d[1][0]), *d[1][1:])
        else:
            return d[0], i_to_f(d[1])
    else:
        dt = np.dtype(d)
        return f"f{dt.alignment}" if dt.kind == "i" else d


def get_mask_from(a: np.ndarray):
    if a.dtype.names is None:
        return np.isnan(a)
    else:
        return np.array(
            list(zip(*(get_mask_from(a[col]) for col in a.dtype.names))),
            np.ma.make_mask_descr(a.dtype)
        )


BunchPhoton_numOfLightIndex = 4

common_data_type = [
    *_util.event_info_dtype_descr,
    ("simu", [
        ("logE0", "f4"),
        ("logNmax", "f4"),
        ("Xmax", "f4"),
        ("Xint", "f4"),
        ("zenith", "f4"),
        ("azimuth", "f4"),
        ("core_position", ("f4", 3)),
        ("Rp", "f4"),
        ("psi", "f4")
    ]),

    ("recon", [
        ("is_triggerd", "?"),
        ("zenith", "f4"),
        ("azimuth", "f4"),
        ("core_position", ("f4", 3)),
        ("timing_fit", [
            ("chi2", "f4"),
            ("ndf", "i4"),
        ]),
        ("logE0", "f4"),
        ("logNmax", "f4"),
        ("Xmax", "f4"),
        ("Xint", "f4"),
        # Slant depth at the start of FD-viewing range 
        ("Xstart", "f4"),
        # Slant depth at the end of FD-viewing range 
        ("Xend", "f4"),
        # ("GH_fit_chi2", "f4"),

        ("Rp", "f4"),
        ("total_photons", "f4"),
        ("time_extent", "f4"),
        ("track_length", "f4"),
        # The number of PMTs (triggered?) at the brightest station.
        ("n_pmts", "i4"),

        ("psi", "f4"),
        ("psi_error", "f4"),
        ("core_distance", "f4"),
        ("core_distance_error", "f4"),
        ("time_at_core", "f4"),
        ("time_at_core_error", "f4"),
        ("minimum_viewing_angle", "f4"),

        # ("GH_fit_chi2", ("f4", 2)),
        ("GH_fit", [
            ("chi2", "f4"),
            ("ndf", "i4")
        ]),
        ("total_photons_derived_from", [
            ("fluorescent", "f4"), ("direct_cherenkov", "f4"),
            ("rayleigh-scattered_cherenkov", "f4"), ("mie-scattered_cherenkov", "f4")
        ]),
        ("n_saturated_pmts", "i4")
    ])
]

mono_recon_extension = [
    ("TripletHasFD", "i4"),
    ("TripletUseFD", "i4")
]

hybrid_recon_extension = [
    ("sd", [
        ("sd_event_code", "i4"),
        ("sd_trigger_mode", "i4"),
        ("numOfTimeCluster", "i4"),
        ("selected", [
            ("sd_id", "i4"),
            ("sdAveMip", "f4"),
            ("sdDistAxis", "f4")
        ]),
        ("maximum_signal", [
            ("sd_id", "i4"),
            ("sdAveMip", "f4"),
            ("sdDistAxis", "f4")
        ])
    ]),
    # 4ring
]

invalid_common_data = np.full(1, np.nan, dtype=i_to_f(common_data_type))[0]

mono_data_type = copy.deepcopy(common_data_type)
mono_data_type[-1] = ("recon", [*common_data_type[-1][1], *mono_recon_extension])

hybrid_data_type = copy.deepcopy(common_data_type)
hybrid_data_type[-1] = ("recon", [*common_data_type[-1][1], *hybrid_recon_extension])


def load(path, time_unit="us", distance_unit="km", mode="mono"):
    if time_unit == "us":
        pass
    else:
        raise ValueError(f"Unexpected time unit '{time_unit}'")

    if distance_unit == "km":
        pass
    else:
        raise ValueError(f"Unexpected distance unit '{distance_unit}'")

    if mode in ("mono", "hybrid"):
        is_mono = mode == "mono"
    else:
        raise ValueError(f"Unexpected mode '{mode}' (mode must be 'mono' or 'hybrid')")

    def _generate():
        for line in open(path, "r"):
            buffer = line.split()
            assert buffer[-1] == "###"
            buffer = buffer[:-1]

            # Before 'simu' at position 6
            # date, time = buffer[4:6]
            # # To ISO format
            # datetime = f"{date.replace('/', '-')}T{time}"
            # # Remove null-strings if exists at first index
            # event_info = (buffer[0], *buffer[1:4], np.datetime64(datetime))
            event_info = _util.parse_event_info(*buffer[:6])

            buffer = buffer[7:]

            # Before 'trig' at position 18
            if all(e == "0" for e in buffer[0:11]):
                # simu_data = tuple([np.nan] * 6 + [[np.nan] * 3] + [np.nan] * 2)
                simu_data = invalid_common_data["simu"]
            else:
                simu_data = *buffer[:6], buffer[6:9], *buffer[9:11]
            buffer = buffer[11:]

            # After 'trig'
            assert buffer[0] == "trig"
            recon1 = [buffer[1]]
            buffer = buffer[2:]

            if np.char.isdigit(buffer[0]) and buffer[0] in ("0", "1"):
                recon1.extend([np.nan, np.nan, [np.nan, np.nan, np.nan], (np.nan, np.nan)])
            else:
                recon1.extend([*buffer[0:2], buffer[2:5], tuple(buffer[5:7])])
                buffer = buffer[7:]

            if buffer[0] == "0":
                recon1.extend([np.nan] * 6)
                buffer = buffer[1:]
            else:
                assert buffer[0] == "1"
                recon1.extend(buffer[1:7])
                buffer = buffer[8:]  # Skip ReconGHFitChi2

            if len(buffer) == 0:
                recon2 = [
                    np.nan, *(np.nan,) * 11, (np.nan, np.nan), (np.nan,) * BunchPhoton_numOfLightIndex,
                    np.nan
                ]
                if is_mono:
                    recon2.extend([np.nan] * 2)
                else:
                    recon2.append((*(np.nan,) * 3, (np.nan,) * 3, (np.nan,) * 3))

            else:
                # assert buffer[1] == buffer[6]
                recon2 = [
                    buffer[0], *buffer[2:13], tuple(buffer[13:15]), tuple(buffer[15:15+BunchPhoton_numOfLightIndex])
                ]
                buffer = buffer[15 + BunchPhoton_numOfLightIndex:]
        
                if len(buffer) == 2:
                    recon2.append(np.nan)
                else:
                    recon2.append(buffer[0])
                    buffer = buffer[1:]

                if is_mono:
                    if len(buffer) != 2:
                        recon2.extend([np.nan] * 2)
                    else:
                        recon2.extend(buffer[0:2])
                        buffer = buffer[2:]
                else:
                    if len(buffer) < 9:
                        recon2.append((*(np.nan,) * 3, (np.nan,) * 3, (np.nan,) * 3))
                    else:
                        sd_info = []
                        sd_info.extend(buffer[0:3])
                        sd_info.append(tuple(buffer[3:6]))
                        sd_info.append(tuple(buffer[6:9]))
                        recon2.append(tuple(sd_info))

                        buffer = buffer[9:]
                        if len(buffer) == 4:
                            # 4ring
                            buffer = []

                if len(buffer) != 0:
                    raise RuntimeError(f"Unexpected values: {buffer}")

            yield *event_info, simu_data, (*recon1, *recon2)

    data_type = mono_data_type if is_mono else hybrid_data_type
    data = np.fromiter(_generate(), i_to_f(data_type))

    return np.ma.MaskedArray(data, get_mask_from(data)).astype(data_type)
