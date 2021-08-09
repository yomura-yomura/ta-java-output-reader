import tajava.plot.fd.signal_map
import tajava.plot.fd.event_display
import tajava.plot.fd.time_vs_angle
import tajava.plot.fd.lateral_dist
import plotly_utility.subplots


__all__ = ["plot", "Plotter"]


def plot(data_path, part, event_number, date, auto_open=True):
    return Plotter(data_path).plot(part, event_number, date, auto_open)


def _plot(
    sdrecon_signal_data, hybridrecon_data,
    long_pmt_3_data, geom_polar_track_data,
    time_vs_angle_data, time_vs_angle_fit_data,
    sdrecon_lateral_density_data,
    auto_open
):
    left_fig = tajava.plot.fd.signal_map._plot(sdrecon_signal_data, hybridrecon_data, auto_open=False)
    right_fig = plotly_utility.subplots.vstack(
        tajava.plot.fd.event_display._plot(long_pmt_3_data, geom_polar_track_data, auto_open=False),
        plotly_utility.subplots.hstack(
            tajava.plot.fd.time_vs_angle._plot(time_vs_angle_data, time_vs_angle_fit_data, auto_open=False),
            tajava.plot.fd.lateral_dist._plot(sdrecon_lateral_density_data, auto_open=False),
            horizontal_spacing=0.175
        )
    )
    fig = plotly_utility.subplots.hstack(left_fig, right_fig, horizontal_spacing=0.1)

    if auto_open:
        fig.show()
    return fig


class Plotter:
    def __init__(self, data_path, render_type="browser", render_options=None):
        assert render_type in ("browser", "mpl_plot")
        self.render_type = render_type
        if render_options is None:
            render_options = dict()
        elif isinstance(render_options, dict):
            pass
        else:
            raise TypeError(type(render_options))
        self.render_options = render_options

        self.sdrecon_signal_data = tajava.reader.fd.sdrecon_signal.load(data_path)
        self.hybridrecon_data = tajava.reader.fd.hybridrecon.load(data_path)

        self.long_pmt_3_data = tajava.reader.fd.long_pmt_3.load(data_path)
        self.geom_polar_track_data = tajava.reader.fd.geom_polar_track_recon4tale.load(data_path)

        self.time_vs_angle_data = tajava.reader.fd.time_vs_angle.load(data_path)
        self.time_vs_angle_fit_data = tajava.reader.fd.time_vs_angle_fit.load(data_path)

        self.sdrecon_lateral_density_data = tajava.reader.fd.sdrecon_lateral_density.load(data_path)

    def plot(self, part, event_number, date, auto_open=True):
        fig = _plot(
            tajava.reader.fd.util.get_matched(self.sdrecon_signal_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.hybridrecon_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.long_pmt_3_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.geom_polar_track_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.time_vs_angle_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.time_vs_angle_fit_data, part, event_number, date),
            tajava.reader.fd.util.get_matched(self.sdrecon_lateral_density_data, part, event_number, date),
            auto_open=False
        )
        fig.layout.title = f"{part}, {event_number}, {date}"
        if auto_open:
            if self.render_type == "browser":
                plotly_utility.offline.plot(
                    fig,
                    filename=self.render_options.get("filename", "temp-plot.html")
                )
            elif self.render_type == "mpl_plot":
                width = self.render_options.get("width", None)
                height = self.render_options.get("height", None)
                if width is None:
                    width = 1200
                if height is None:
                    height = 600
                plotly_utility.offline.mpl_plot(
                    fig, width, height, self.render_options.get("scale", 1)
                )
        return fig
