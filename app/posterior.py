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


def posterior_plot(x, y1, y2, lower_bound, upper_bound):

    fig = go.Figure()

    fig.add_trace(
        go.Line(
            x = x,
            y = y1,
            line_color = bolttech_colors['cyan_dark'],
            name = 'Control'
        )
    )

    fig.add_trace(
        go.Line(
            x = x,
            y = y2,
            line_color = bolttech_colors['blue_dark'],
            name = 'Test'
        )
    )

    fig.update_layout(
        width = 800,
        height = 600,
        title="Conversion Probability",
        xaxis_title="Conversion Rate",
<<<<<<< HEAD
        # yaxis_title="Density",
=======
>>>>>>> c57da23 (Merge branch 'develop' of https://github.com/peterlee-bolttech/peterlee-bolttech into develop)
        showlegend= True,
        xaxis_range=[lower_bound, upper_bound]
    )
    
    fig.update_yaxes(visible = False)

    fig.update_yaxes(visible = False)

    return fig