#!/usr/bin/env python3
import argparse
import tajava.reader.tale

p = argparse.ArgumentParser()
p.add_argument("tale_java_output")
args = p.parse_args()

data = tajava.reader.tale.load(args.tale_java_output)

import plotly.express as px

print("drawing energy dist")
fig = px.histogram(
    x=data["recon"]["logE0"],
    marginal="rug",
    labels={"x": "logE0"}
)
fig.show()

print("drawing θ dist")
fig = px.histogram(
    x=data["recon"]["zenith"],
    marginal="rug",
    labels={"x": "zenith angle"}
)
fig.layout.xaxis.ticksuffix = "°"
fig.show()

print("drawing φ dist")
fig = px.histogram(
    x=data["recon"]["azimuth"],
    marginal="rug",
    labels={"x": "azimuthal angle"}
)
fig.layout.xaxis.ticksuffix = "°"
fig.show()
