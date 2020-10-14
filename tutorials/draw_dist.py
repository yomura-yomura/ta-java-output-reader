#!/usr/bin/env python3
import argparse
import tajava.reader.tale

p = argparse.ArgumentParser()
p.add_argument("tale_java_output")
args = p.parse_args()

data = tajava.reader.tale.load(args.tale_java_output)

import plotly.express as px
import numpy as np

# 視野角内カット
mask = (data["recon"]["Xstart"] < data["recon"]["Xmax"]) & (data["recon"]["Xmax"] < data["recon"]["Xend"])
data = data[mask]
print(f"* Remove {np.count_nonzero(~mask)} events")

if False:
    print("drawing obs-date dist")
    x, counts = np.unique(data["t0"].astype("datetime64[D]"), return_counts=True)
    fig = px.bar(
        x=x,
        y=counts,
        labels={"x": "obs date"}
    )
    fig.show()

if True:
    print("drawing energy dist")
    fig = px.histogram(
        x=data["recon"]["logE0"],
        marginal="rug",
        labels={"x": "logE0"},
        log_y=True
    )
    fig.show()

if False:
    print("drawing θ dist")
    fig = px.histogram(
        x=data["recon"]["zenith"],
        marginal="rug",
        labels={"x": "zenith angle"}
    )
    fig.layout.xaxis.ticksuffix = "°"
    fig.show()

if False:
    print("drawing φ dist")
    fig = px.histogram(
        x=data["recon"]["azimuth"],
        marginal="rug",
        labels={"x": "azimuthal angle"}
    )
    fig.layout.xaxis.ticksuffix = "°"
    fig.show()
