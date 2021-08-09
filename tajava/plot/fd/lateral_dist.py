import numpy as np
import tajava.reader.fd.sdrecon_lateral_density
import plotly.express as px
import plotly.graph_objs as go
# try:
#     import pyrecon.analyzer.ldf
#     is_niche_lib_found = True
# except ImportError:
#     is_niche_lib_found = False


def _plot(sdrecon_lateral_density_data, auto_open):
    fig = px.scatter(
        x=sdrecon_lateral_density_data["r"] * 1e-2,
        y=sdrecon_lateral_density_data["Q"],
        labels={"x": "Distance from Shower Axis", "y": "Number of Photons [cm⁻²]"},
        log_y=True
    ).update_xaxes(ticksuffix=" m", rangemode="tozero")
    fig.update_yaxes(range=(0, np.log10(sdrecon_lateral_density_data["Q"].max()) * 1.1))

    # if is_niche_lib_found:
    #     pyrecon.analyzer.ldf.get_b2

    if auto_open:
        fig.show()
    return fig
