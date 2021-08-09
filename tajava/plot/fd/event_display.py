import pathlib
import numpy as np
import tajava.reader.fd.util
import tajava.reader.fd.geom_polar_track_recon4tale
import tajava.reader.fd.long_pmt_3
import plotly.graph_objs as go
import plotly.express as px
import plotly_utility


__all__ = ["plot"]


def plot(data_path, part, event_number, date, auto_open=True):
    data_path = pathlib.Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(data_path)

    long_pmt_3_data = tajava.reader.fd.long_pmt_3.load(data_path)
    geom_polar_track_data = tajava.reader.fd.geom_polar_track_recon4tale.load(data_path)
    return _plot(
        long_pmt_3_data=tajava.reader.fd.util.get_matched(long_pmt_3_data, part, event_number, date),
        geom_polar_track_data=tajava.reader.fd.util.get_matched(geom_polar_track_data, part, event_number, date),
        auto_open=auto_open
    )


def _plot(long_pmt_3_data, geom_polar_track_data, auto_open):
    pmt_data = long_pmt_3_data.copy()
    # long_pmt_3_data["t"] /= 1000
    long_pmt_3_data = long_pmt_3_data[long_pmt_3_data["flag"] != 0]


    def get_hover_template(npe=False, t=False):
        hover_template_lines = [
            "Azimuthal Angle=%{x}°",
            "Elevation Angle=%{y}°"
        ]
        if npe:
            hover_template_lines.append("Number of Photoelectron=%{marker.size}")
        if t:
            hover_template_lines.append("Time [ns]=%{marker.color}")
        return "{}".format("<br>".join(hover_template_lines))

    fig = px.scatter(
        pmt_data[~np.isin(pmt_data[["site_id", "camera_id", "pmt"]], long_pmt_3_data[["site_id", "camera_id", "pmt"]])],
        x="alpha", y="elev"
    ).update_traces(
        name="PMTs",
        marker=dict(size=1.5, symbol="cross-thin", line=dict(width=2, color="#cccccc"), color="#cccccc"),
        hovertemplate=get_hover_template()
    )
    fig.add_trace(
        go.Scattergl(
            name="Hit PMTs",
            mode="markers",
            x=long_pmt_3_data[long_pmt_3_data["flag"] == 1]["alpha"],
            y=long_pmt_3_data[long_pmt_3_data["flag"] == 1]["elev"],
            marker=dict(
                line_width=0,
                color=long_pmt_3_data[long_pmt_3_data["flag"] == 1]["t"] - long_pmt_3_data[long_pmt_3_data["flag"] == 1]["t"].min(),
                colorbar=dict(
                    title="Time [ns]"
                ),
                colorscale="Portland",
                sizemode="area",
                size=long_pmt_3_data[long_pmt_3_data["flag"] == 1]["npe"],
                sizeref=2 * long_pmt_3_data["npe"].max() / (20 ** 2),
                sizemin=3,
                opacity=1
            ),
            hovertemplate=get_hover_template(npe=True, t=True)
        )
    )
    fig.add_trace(
        go.Scattergl(
            name="Unused PMTs",
            mode="markers",
            x=long_pmt_3_data[long_pmt_3_data["flag"] < 0]["alpha"],
            y=long_pmt_3_data[long_pmt_3_data["flag"] < 0]["elev"],
            marker=dict(
                sizemode="area",
                size=long_pmt_3_data[long_pmt_3_data["flag"] < 0]["npe"],
                sizeref=2 * long_pmt_3_data["npe"].max() / (20 ** 2),
                sizemin=3,
                color="white"
            ),
            hovertemplate=get_hover_template(npe=True)
        )
    )
    # fig = px.scatter(
    #     long_pmt_3_data[long_pmt_3_data["flag"] == 1],
    #     x="alpha", y="elev",
    #     color="t", size="npe",
    #     size_max=10,
    #     labels={"t": "Time [ns]",
    #             "alpha": "Azimuthal Angle", "elev": "Elevation Angle", "npe": "Number of Photoelectron"}
    #     # color_continuous_scale=px.colors.diverging.Picnic
    # ).update_xaxes(ticksuffix="°").update_yaxes(ticksuffix="°")
    # trace = fig.data[0]
    # trace.marker.symbol = ["cross-thin" if size == 0 else "circle" for size in trace.marker.size]
    # trace.marker.line.width = [2 if size == 0 else 0 for size in trace.marker.size]
    # trace.marker.line.color = "gray"
    # colors = [
    #     "white" if np.isnan(time) and size > 0 else time
    #     for size, time in zip(trace.marker.size, trace.marker.color)
    # ]
    # trace.marker.color = None  # to suppress numpy warning
    # trace.marker.color = colors
    # trace.marker.size += 3

    fig.add_trace(
        go.Scattergl(
            mode="lines",
            x=geom_polar_track_data["azimuth"] + 360, y=geom_polar_track_data["zenith"],
            line=dict(color="#EF553B")
        )
    )
    # use_colorbar_in_trace(fig)

    fig.update_xaxes(range=(95, 225))
    fig.update_yaxes(range=(0, 65))
    fig.update_traces(showlegend=False)

    traces = [trace for trace in fig.data if len(trace.marker.colorbar.to_plotly_json()) > 0]
    fig.layout.xaxis.domain = (0, 1 - 0.1 * len(traces))
    for i, trace in enumerate(traces):
        trace.marker.colorbar.x = 1 - 0.1 * i
        trace.marker.colorbar.y = 0.5
        trace.marker.colorbar.xanchor = "center"
        trace.marker.colorbar.yanchor = "middle"

    if auto_open:
        fig.show()
    return fig


def use_colorbar_in_trace(fig):
    colorscale = fig.layout.coloraxis.pop("colorscale")
    colorbar = fig.layout.coloraxis.pop("colorbar")
    for trace in fig.data:
        if trace.marker.coloraxis is not None:
            trace.marker.coloraxis = None
            trace.marker.colorscale = colorscale

            if colorbar.x is None:
                colorbar.x = 0.95
            if colorbar.y is None:
                colorbar.y = 1
            if colorbar.xanchor is None:
                colorbar.xanchor = "left"
            if colorbar.yanchor is None:
                colorbar.yanchor = "top"
            if colorbar.len is None:
                colorbar.len = 1
            plotly_utility.subplots._scale_all_objects(fig, "right", fraction=0.95, spacing=0)
            trace.marker.colorbar = colorbar.to_plotly_json()
    return fig

