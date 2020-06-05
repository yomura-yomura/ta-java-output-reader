import numpy as np

invalid_value = np.nan
BunchPhoton_numOfLightIndex = 4

data_type = [
    ("detector_type", "i2"),
    ("fd_type", "i2"),
    ("part", "i4"),
    ("event_number", "i4"),
    ("t0", "M8[ns]"),

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
        ("chi2", "f4"),
        ("ndf", "f4"),  # Should be integer?
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
        ("psi", "f4"),
        ("total_photons", "f4"),
        ("time_extent", "f4"),
        ("track_length", "f4"),
        # The number of PMTs (triggered?) at the brightest station.
        ("n_pmts", "f4"),  # Should be integer but there is no int-type nan for missing values.
        ("psi_error", "f4"),
        ("core_distance", "f4"),
        ("core_distance_error", "f4"),
        ("time_at_core", "f4"),
        ("time_at_core_error", "f4"),
        ("minimum_viewing_angle", "f4"),
        ("GH_fit_chi2", ("f4", 2)),
        ("total_photons_derived_from", ("f4", BunchPhoton_numOfLightIndex)),
        ("n_saturated_pmts", "f4"),  # Should be integer
        ("TripletHasFD", "f4"),  # Should be integer
        ("TripletUseFD", "f4")  # Should be integer
    ])
]


def load(fn, time_unit="us", distance_unit="km"):
    if time_unit == "us":
        pass
    else:
        raise ValueError(f"Unexpected time unit '{time_unit}'")
    if distance_unit == "km":
        pass
    else:
        raise ValueError(f"Unexpected distance unit '{distance_unit}'")
    
    def _generate():
        for line in open(fn, "r"):
            buffer = line.split()
            assert buffer[-1] == "###"
            buffer = buffer[:-1]

            # Before 'simu' at position 6
            date, time = buffer[4:6]
            datetime = f"{date.replace('/', '-')}T{time}"  # To ISO format
            event_info = (*buffer[:4], np.datetime64(datetime))
            buffer = buffer[7:]

            # Before 'trig' at position 18
            simu_data = *buffer[:6], buffer[6:9], *buffer[9:11]
            buffer = buffer[11:]

            # After 'trig'
            assert buffer[0] == "trig"
            recon1 = [buffer[1]]
            buffer = buffer[2:]

            if np.char.isdigit(buffer[0]) and buffer[0] in ("0", "1"):
                recon1.extend([invalid_value] * 2 + [[invalid_value] * 3] + [invalid_value] * 2)
            else:
                recon1.extend([*buffer[0:2], buffer[2:5], *buffer[5:7]])
                buffer = buffer[7:]

            if buffer[0] == "0":
                recon1.extend([invalid_value] * 6)
                buffer = buffer[1:]
            else:
                assert buffer[0] == "1"
                recon1.extend(buffer[1:7])
                buffer = buffer[8:]

            if len(buffer) == 0:
                recon2 = (
                        [invalid_value] * 12 +
                        [[invalid_value] * 2] +
                        [[invalid_value] * BunchPhoton_numOfLightIndex] +
                        [invalid_value] +
                        [invalid_value] * 2
                )
            else:
                # assert buffer[1] == buffer[6]
                recon2 = [buffer[0], *buffer[2:13], buffer[13:15], buffer[15:15+BunchPhoton_numOfLightIndex]]
                buffer = buffer[15 + BunchPhoton_numOfLightIndex:]
        
                if len(buffer) == 2:
                    recon2.append(invalid_value)
                else:
                    recon2.append(buffer[0])
                    buffer = buffer[1:]

                if len(buffer) != 2:
                    recon2.extend([invalid_value] * 2)
                else:
                    recon2.extend(buffer[0:2])
                    buffer = buffer[2:]

                assert len(buffer) == 0

            yield *event_info, simu_data, (*recon1, *recon2)

    return np.fromiter(_generate(), data_type)
