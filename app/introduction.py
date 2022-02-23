import code
from ctypes import cdll
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from bokeh.plotting import figure
import plotly.graph_objs as go
import scipy.stats as scs
import scipy

bolttech_colors = {
        'white': '#FFFFFF',
        'black': '#000000',
        'blue_dark': '#160E45',
        'cyan_dark': '#00B9C7',
        'cyan_medium': '#66D6DD',
        'cyan_light': '#CCF1F3',
        'yellow_dark': '#E2D900',
        'yellow_light': '#F9F7CC',
        'grey_dark': '#746F95',
        'grey_light': '#D1CFDC'
        }


def intro_plot(pA, pB, nA, nB, alpha):
    # pA = 0.1
    # pB = 0.13

    sA = np.sqrt(pA * (1 - pA)) / np.sqrt(nA)
    sB = np.sqrt(pB * (1 - pB)) / np.sqrt(nB)

    xA = np.linspace(0, 2 * pA, 1000)
    xB = np.linspace(0, 2 * pB, 1000)

    yA = scs.norm(pA, sA).pdf(xA)
    yB = scs.norm(pB, sB).pdf(xB)

    zscore = scipy.stats.norm.ppf(1 - alpha/2)

    upper_boundA = pA + zscore * np.sqrt(pA * (1 - pA) / nA)

    xC = xB.copy()
    yC = yB.copy()
    count = (xC < upper_boundA).sum()
    yC[:count] = 0

    xD = xB.copy()
    yD = yB.copy()
    count = (xD < upper_boundA).sum()
    yD[count:] = 0

    xE = xA.copy()
    yE = yA.copy()
    count = (xE < upper_boundA).sum()
    yE[:count] = 0


    fig = go.Figure()

    fig.add_trace(go.Line(x = xA, y = yA, line_color = bolttech_colors['cyan_dark'], name = 'Null'))
    fig.add_trace(go.Line(x = xB, y = yB, line_color = bolttech_colors['yellow_dark'], name = 'Alternative'))
    fig.add_trace(go.Line(x = xC, y = yC, line_color = bolttech_colors['cyan_medium'], fill = 'toself', line_width = 0.01, name = 'Statistical Power'))
    fig.add_trace(go.Line(x = xD, y = yD, line_color = bolttech_colors['yellow_light'], fill = 'toself', line_width = 0.01, name = 'Beta Area'))
    fig.add_trace(go.Line(x = xE, y = yE, line_color = bolttech_colors['grey_dark'], fill = 'toself', line_width = 0.01, name = 'Alpha Area'))




    fig.update_layout(
        width = 800,
        height = 600,
        title="Statistical Power: by Sample size",
        xaxis_title="Converted Proportion",
)

    fig.add_vline(x=upper_boundA, line_width=2, line_dash="dash", line_color="grey")
    fig.add_annotation(align = 'left', showarrow=False, x = 0.04, y = yB.max() * 0.95, text = 'Statistical Power: {0:.1f} %'.format((1 - scs.norm(pB, sB).cdf(upper_boundA)) * 100))
    fig.add_annotation(align = 'left', showarrow=False, x = 0.04, y = yB.max() * 0.85, text = 'Beta Level       : {0:.1f} %'.format((scs.norm(pB, sB).cdf(upper_boundA)) * 100))
    fig.add_annotation(align = 'left', showarrow=False, x = 0.04, y = yB.max() * 0.75, text = 'Alpha Level       : {0:.1f} %'.format((1- scs.norm(pA, sA).cdf(upper_boundA)) * 100))

    return fig