import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import scipy.stats as scs
# from scipy.stats import beta


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


def heatmap_plot(df_matrix, title="Control/Treatment group conversion matrix"):
    """Generate heatmap figure from NxN matrix.

    Args:
        df_matrix (pandas.DataFrame): Matrix as DataFrame. Index values and column values must be equal.
        title (str): Title of plot. Defaults to "".

    Returns:
        plotly.graph_objs.Figure

    """
    trace = go.Heatmap(
        z=df_matrix,
        x=df_matrix.columns,
        y=df_matrix.index,
        hovertemplate='%{y} ---> %{x}<extra>%{z}</extra>',
        colorscale= 'blues'
    )
    
    data = [trace]
    layout = {
        'title': {'text': title},
        'xaxis': {'title': "control_cr"},
        'yaxis': {'title': "treatment_cr"}
    }

    fig = go.Figure(data=data, layout=layout)

    return fig 