import numpy as np

import tajava.reader.fd.time_vs_angle
import tajava.reader.fd.time_vs_angle_fit
import plotly.express as px
import plotly.graph_objs as go


def _plot(time_vs_angle_data, time_vs_angle_fit_data, auto_open):
    assert len(time_vs_angle_fit_data) == 1
    time_vs_angle_fit_data = time_vs_angle_fit_data[0]

    fig = px.scatter(
        x=np.rad2deg(time_vs_angle_data["alpha"]),
        y=(time_vs_angle_data["t"] - time_vs_angle_data["t"].min()) / 1000, error_y=time_vs_angle_data["t_err"] / 1000,
        color=time_vs_angle_data["station_id"].astype(str),
        color_discrete_sequence=["orange", "red", "blue"],
        category_orders={"color": ["0", "1", "3"]},
        labels={"x": "Azimuthal Angle", "y": "Time [μs]", "color": "Station ID"}
    ).update_xaxes(ticksuffix="°")
    fig.update_traces(showlegend=False)

    x = np.arange(-20, 80, 1)
    y = tajava.reader.fd.time_vs_angle_fit.timing_fit(np.deg2rad(x), *time_vs_angle_fit_data[["tau0", "Rp", "psi"]])
    y -= time_vs_angle_data["t"].min()
    fig.add_trace(
        go.Scattergl(
            mode="lines", name="Timing Fit",
            x=x, y=y / 1000,
            showlegend=False,
            line=dict(color="#EF553B")
        )
    )

    if auto_open:
        fig.show()
    return fig
