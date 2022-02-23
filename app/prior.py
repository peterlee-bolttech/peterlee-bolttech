import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import plotly.graph_objs as go
import scipy.stats as scs
from scipy.stats import beta

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

def prior_plot(x, y):
    """Diplays a bar chart of conversion rates of A/B test groups,
    with the y-axis denoting the conversion rates.
    Parameters
    ----------
    df: pd.DataFrame
        The source DataFrame containing the data to be plotted
    Returns
    -------
    streamlit.altair_chart
        Bar chart with text above each bar denoting the conversion rate
    """

    fig = go.Figure()

    fig.add_trace(
            go.Line(
                x = x,
                y = y,
                line_color = bolttech_colors['cyan_dark'],
                name = 'Null'
            )
        )

    fig.update_layout(
            width = 800,
            height = 600,
            title="Conversion Probability",
            xaxis_title="Chosen Prior",
            yaxis_title="Density",
            showlegend= True
        )

    return fig