import plotly_utility
import numpy as np
import tajava.plot.fd.niche_tale_event_display


if __name__ == "__main__":
    data_path = "/Users/yomura/Study/niche/hybrid_analysis/fd_data/hybrid/sim/sim_hybrid_06/recon/DAT100000/data"

    part = 0
    event_number = 0
    date = np.datetime64("2017-01-01")
    plotter = tajava.plot.fd.niche_tale_event_display.Plotter(data_path, render_type="mpl_plot")
    # plotter = tajava.plot.fd.niche_tale_event_display.Plotter(data_path)

    for i in range(10):
        plotter.plot(part, i, date)
