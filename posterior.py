from __future__ import annotations
import plotly.graph_objs as go
import numpy as np

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
        go.Scatter(
            x = x,
            y = y1,
            line_color = bolttech_colors['cyan_dark'],
            name = 'Control'
        )
    )

    fig.add_trace(
        go.Scatter(
            x = x,
            y = y2,
            line_color = bolttech_colors['blue_dark'],
            name = 'Test'
        )
    )

    # where test > control
    vline = np.where(y1 < y2)[0][0]
    fig.add_vline(x=x[vline], line_width=2, line_dash="dash", line_color="grey")

    y3 = y2.copy()
    y3[:vline] = 0

    fig.add_trace(
        go.Scatter(
            x = x,
            y = y3,
            line_color = bolttech_colors['blue_dark'],
            name = 'Test > Control',
            fill = 'toself',
            line_width = 0.01
        )
    )

    fig.update_layout(
        width = 800,
        height = 600,
        title="Conversion Probability",
        xaxis_title="Conversion Rate",
        showlegend= True,
        xaxis_range=[lower_bound, upper_bound],
    )
        
    # fig.add_annotation(align = 'right', showarrow=False, x = (lower_bound + upper_bound)/2, y = y2.max() * 0.99,
    # text = 'Probability of upperhand group being better than the rest is {0:.1f} %'.format(y3.sum()/len(x) * 100))

    fig.update_yaxes(visible = False)

    return fig