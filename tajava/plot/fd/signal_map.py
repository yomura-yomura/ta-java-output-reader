import numpy as np
import tajava.reader.fd.sdrecon_signal
import tajava.reader.fd.hybridrecon
import plotly.express as px
import plotly.graph_objs as go
import pathlib
import numpy_utility as npu


coordinate_path = pathlib.Path(__file__).resolve().parent / "coordinate"

sd_positions = npu.to_tidy_data({
    "TALE SD": np.loadtxt(coordinate_path / "talesd.txt", dtype=[("lid", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")]),
    "NICHE": np.loadtxt(coordinate_path / "niche.txt", dtype=[("lid", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")]),
    "TA SD": np.loadtxt(coordinate_path / "tasd.txt", dtype=[("lid", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")]),
}, "SD Type", ("lid", "x", "y", "z"))
sd_positions["x"] *= 1e-3
sd_positions["y"] *= 1e-3

md_tale_fd_pos = np.loadtxt(coordinate_path / "MD-TALE_site.dat", dtype=[("x", "f8"), ("y", "f8"), ("z", "f8")])
md_tower_pos = np.loadtxt(coordinate_path / "mdtower.txt", dtype=[("lid", "i4"), ("x", "f8"), ("y", "f8"), ("z", "f8")])
md_tower_pos["x"] *= 1e-3
md_tower_pos["y"] *= 1e-3


def _plot(sdrecon_signal, hybridrecon_data, auto_open, show_id=False):
    fig = px.scatter(
        sd_positions, x="x", y="y", text="lid", color="SD Type",
        labels={"x": "X (West to East)", "y": "Y (South to North)", "lid": "SD ID"},
        color_discrete_sequence=["#666666"]
    )
    if show_id == np.False_:
        fig.update_traces(mode="markers")
    fig.update_traces(marker_symbol="square-open")
    fig.update_traces(marker_size=10, selector=dict(name="NICHE"))
    fig.update_traces(marker_size=12, selector=dict(name="TALE SD"))
    fig.update_traces(marker_size=14, selector=dict(name="TA SD"))
    fig.update_xaxes(scaleanchor="y", scaleratio=1, constrain="domain", ticksuffix=" km")
    fig.update_yaxes(ticksuffix=" km")

    fig.add_trace(
        go.Scatter(
            name="MD-TALE FD",
            text="MD-TALE FD",
            mode="markers+text",
            x=md_tale_fd_pos["x"], y=md_tale_fd_pos["y"],
            marker=dict(symbol="star", size=15, line_width=0, color="#666666"),
            textposition="middle left"
        )
    )

    fig.add_trace(
        go.Scattergl(
            name="Hit Detectors",
            mode="markers",
            x=sdrecon_signal["x"] * 1e-5,
            y=sdrecon_signal["y"] * 1e-5,
            marker=dict(
                line_width=0,
                color=(sdrecon_signal["t"] - sdrecon_signal["t"].min()) * 1000,
                colorbar=dict(
                    title="Time [ns]"
                ),
                colorscale="Portland",
                sizemode="area",
                size=sdrecon_signal["Q"],
                sizeref=2 * sdrecon_signal["Q"].max() / (20 ** 2),
                # sizemin=5,
                opacity=1
            ),
            # hovertemplate=get_hover_template(npe=True, t=True)
        )
    )

    for hybridrecon_row in hybridrecon_data:
        azimuth = np.deg2rad(180 - (hybridrecon_row["azimuth"] - 90))
        arrow = 0.2 * np.array([np.cos(azimuth), np.sin(azimuth)])
        arrow_perp = 0.1 * np.array([np.cos(azimuth + np.pi/2), np.sin(azimuth + np.pi/2)])

        color = "magenta" if hybridrecon_row["is_true"] else "black"

        fig.add_trace(
            go.Scattergl(
                name="{} Core Position".format("True" if hybridrecon_row["is_true"] else "Reconstructed"),
                x=[hybridrecon_row["x"]], y=[hybridrecon_row["y"]],
                marker_color=color,
                opacity=0
            )
        )
        add_arrow_shape(
            fig,
            x0=hybridrecon_row["x"] - arrow[0] * 0.5, x1=hybridrecon_row["x"] + arrow[0] * 0.5,
            y0=hybridrecon_row["y"] - arrow[1] * 0.5, y1=hybridrecon_row["y"] + arrow[1] * 0.5,
            line=dict(color=color, width=3)
        )
        fig.add_shape(
            type="line",
            x0=hybridrecon_row["x"] - arrow_perp[0] * 0.5, x1=hybridrecon_row["x"] + arrow_perp[0] * 0.5,
            y0=hybridrecon_row["y"] - arrow_perp[1] * 0.5, y1=hybridrecon_row["y"] + arrow_perp[1] * 0.5,
            line=dict(color=color, width=3)
        )

    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=(-8, -6))
    fig.update_yaxes(range=(17.75, 19.75))

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


def add_arrow_shape(fig, x0, y0, x1, y1, **kwargs):
    theta = np.arctan2(y1 - y0, x1 - x0)
    arrow_length = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    right_arrow = -0.25 * arrow_length * np.array([np.cos(theta - np.deg2rad(30)), np.sin(theta - np.deg2rad(50))])
    left_arrow = -0.25 * arrow_length * np.array([np.cos(theta + np.deg2rad(30)), np.sin(theta + np.deg2rad(50))])

    fig.add_shape(
        type="line",
        x0=x0, y0=y0, x1=x1, y1=y1,
        editable=False,
        **kwargs
    )
    fig.add_shape(
        type="line",
        x0=x1, y0=y1, x1=x1 + right_arrow[0], y1=y1 + right_arrow[1],
        editable=False,
        **kwargs
    )
    fig.add_shape(
        type="line",
        x0=x1, y0=y1, x1=x1 + left_arrow[0], y1=y1 + left_arrow[1],
        editable=False,
        **kwargs
    )
