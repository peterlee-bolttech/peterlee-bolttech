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


def barplot(results, sampleSize, Converted):

    results['conversionRate'] = round(results['conversionRate'] * 100, 2)
    results['conversionRate'] = results['conversionRate'].apply(lambda x: 'Conversion Rate: ' + str(x) + str(' %'))
    
    branches = [
        [*results['conversionRate']],
        [*results.index]
    ]
    
    phoneSales = results[sampleSize]
    protectionSales = results[Converted]

    trace1 = go.Bar(
    x = branches,
    y = phoneSales,
    name = sampleSize,
    marker_color = bolttech_colors['grey_dark'])

    trace2 = go.Bar(
    x = branches,
    y = protectionSales,
    name = Converted,
    marker_color = bolttech_colors['yellow_dark'])

    data = [trace1, trace2]
    layout = go.Layout(barmode = 'group')
    fig = go.Figure(data = data, layout = layout)

    fig.update_layout(
        width = 700,
        height = 500,
        # title="Data Summary Visual",
        yaxis_title="Record Count",
        showlegend= True,
    )

    return fig