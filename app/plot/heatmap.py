import numpy as np
import plotly.graph_objs as go


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


def heatmap_plot(df_matrix, title=""):
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
        colorscale= 'darkmint'
    )

    lower_bound = df_matrix.columns.min()
    upper_bound = df_matrix.columns.max()
    
    data = [trace]
    layout = {
        'title': {'text': title},
        'xaxis': {'title': "Control Group Conversion Rate"},
        'yaxis': {'title': "Test Group Conversion Rate"}
    }

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
            width = 550,
            height = 500,
            xaxis_range=[lower_bound, upper_bound],
            yaxis_range=[lower_bound, upper_bound],
            margin=dict(l=0, r=0, t=0, b=0)
)

    fig.add_trace(
        go.Scatter(
            x = np.linspace(lower_bound, upper_bound, 100),
            y = np.linspace(lower_bound, upper_bound, 100),
            line_color = bolttech_colors['blue_dark'])
            )

    return fig 