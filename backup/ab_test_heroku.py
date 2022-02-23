import dash
import dash_core_components as dcc
import dash_html_components as html
import scipy.stats as scs
import scipy.stats as st
import numpy as np
import plotly.graph_objs as go

from dash.dependencies import Input, Output
from scipy.stats import norm, zscore

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "bolttech-abtest"

ALLOWED_TYPES = (
                'number', 'number', 'range', 'range'
            )


app.layout = html.Div([
    html.Nav(
        style = {'backgroundColor': '#00BAC7',
        # 'width': '800px',
        'height': '70px'
        },
        children = [
            html.A(
                href = "https://bolttech.io",
                children = [
                    html.Img(src = 'https://www.datocms-assets.com/24091/1590561811-bolttech-logo.svg',
                            style = {'width': '80px',
                                    'height': '50px',
                                    'display': 'd-inline-block align-top',
                                    'margin': '10px'})
                ]
                

                        
            )]),

    html.Br(),

    html.Div([

        ## Plot part
        html.Div(
            style = {'width': '45%',
                    'position': 'flex',
                    'left': '2%',
                    'display': 'inline-block',
                    'top': '10%'},
            children = [

                html.H2(
                    children='Introduction to A/B Test',
                    style = {'textAlign': 'center',
                            'color': '#00B9C7'
                }),

                html.Br(),

                html.P(
                    children = """
                    The graph shows how sample size affects statistical power.
                    """),


                html.P(
                    children = """
                    Imagine you have 10% Of conversion rate under Business as usual and new marketing design has 13% Of conversion rate.\n
                    Is this result statistically meaningful?
                    """),

                html.P(
                    children = """
                    In usual practice, you are expected to have minimum 80% Of statistical power.
                    """),

                html.P(
                    children = """
                    Play around different sample size with slider at the bottom of the page and see how sample size affects statistical power :)\n
                    """),

                dcc.Graph(id="graph"),

                html.Br(),

                html.P(
                    children = "Slider: Sample Size A"),

                dcc.Slider(
                    id='slider1', 
                    min=100, max=1000, value=100, step=10,
                    marks={i: 'Label {}'.format(i) if i == 100 else str(i) for i in range(100, 1001, 100)}),

                html.P(
                    children = "Slider: Sample Size B"),

                dcc.Slider(
                    id='slider2', 
                    min=100, max=1000, value=100, step=10,
                    marks={i: 'Label {}'.format(i) if i == 100 else str(i) for i in range(100, 1001, 100)}),

                html.P(
                    children = "Slider: Alpha level"),

                dcc.Slider(
                    id='slider3', 
                    min=0.01, max=0.5, value=0.05, step=0.01,
                    marks={i: 'Level {}'.format(i) if i == 0.01 else str(i) for i in [0.1, 0.2, 0.3, 0.4, 0.5]}
                    ),

                html.P(
                    children = ["""
                    * Both the are under the hypothesis is 1.
                    """]),
                    
                html.P(
                    children = ["""
                    * Statistical Power = True Positive (THE BIGGER, THE BETTER) - The rate we say 'Yes' and it's true. In other words,
                    statistical power is a chance that we conclude there is a difference between performance of template A and B when there is a actual differnce.
                    In our example, template B achieving 13% Of conversion rate is not by a chance, and we conclude that there is a difference between the two.
                    """]),                
                    
                html.P(
                    children = ["""
                    * Beta level = False Negative (THE SMALLER, THE BETTER)- The rate we say 'No' but it's false. In other words,
                    there is actual difference between performacne of template A and B, but we conclude there is not.
                    In our example, template B achieving 13% Of conversion rate is not by a chance, however, we conclude it happened by a chance.
                    """]),

                html.P(
                    children = ["""
                    * Alpha level =  Significance level - The rate we say 'Yes', but it's false. For our example,
                    there is no actual difference between performance of A and B, but we conclude there is.
                    In our example, template B achieving 13% Of conversion rate is by a chance, however, we think it happened by a chance and conclude it's driven by a coincidence.
                    """])

                ])
        ]
        ),

        ## Sample size part
        html.Div(
            style = {'width': '45%',
                    'position': 'fixed',
                    'left': '53%',
                    'display': 'inline-block',
                    'top': '10%'},
            children = [
            html.H2(
                    children='Sample size calculator',
                    style = {'textAlign': 'center',
                            'color': '#00B9C7'
                }),
                
            html.Br(),

            html.H5(children = 'Baseline conversion rate(%):'),
            html.P(children = 'Conversion Rate at current practice. Please type conversion rate BEFORE making any changes.'),

            dcc.Input(
                id='baseline',
                type='number',
                value = 10,
                min = 1, max = 100, step = 1,
                placeholder="Input Baseline (%)"),

            html.Br(),

            html.H5(children = 'Minimum Detactable Effect(%):'),
            html.P(children = 'The smallest improvement you are willing to be able to detect. In our example, it is 3 since we observe 3 percent improvement to current practice. You want to see this 3 percent of improvement is statistically meaningful or not.'),

            dcc.Input(
                id='MDE',
                type='number',
                value = 3,
                min = 1, max = 100, step = 1,
                placeholder="Input minimum diff to baseline(%):"),

            html.Br(),

            html.H5(children = 'Statistical power (1-beta)(%)'),

            dcc.Input(
                id='stat_power',
                type='number',
                min=1, max=99, value=80, step=1,
                placeholder="Statistical Power (%)"),

            html.Br(),

            html.H5(children = 'Significance level alpha (%):'),

            dcc.Input(id='alpha', value=5, type='number'),

            html.Hr(),

            html.H3(children = 'Minimum size of samples you need for the test is:',
            style = {'textAlign': 'center'}),

            html.H1(id='my-output',
            style = {'textAlign': 'center',
            'color': bolttech_colors['blue_dark']}),
            ]),

            html.Hr(),
        ])

@app.callback(
    [
    Output('graph', 'figure'),
    Output('my-output', 'children')
    ],
    [
    Input('slider1', 'value'),
    Input('slider2', 'value'),
    Input('slider3', 'value'),
    Input('baseline', 'value'),
    Input('MDE', 'value'),
    Input('stat_power', 'value'),
    Input('alpha', 'value')
    ]
    )
    
def multi_output(nA, nB, alpha, baseline, MDE, stat_power, alpha2):

    pA = 0.1
    pB = 0.13

    sA = np.sqrt(pA * (1 - pA)) / np.sqrt(nA)
    sB = np.sqrt(pB * (1 - pB)) / np.sqrt(nB)

    xA = np.linspace(0, 2 * pA, 1000)
    xB = np.linspace(0, 2 * pB, 1000)

    yA = scs.norm(pA, sA).pdf(xA)
    yB = scs.norm(pB, sB).pdf(xB)

    zscore = st.norm.ppf(1 - alpha/2)

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


    baseline = baseline / 100
    MDE = MDE / 100
    stat_power = stat_power / 100
    alpha2 = alpha2 / 100
    p2 = baseline + MDE

    z = norm.isf([alpha2/2]) #two-sided t test
    zp = -1 * norm.isf([stat_power]) 
    s =2*((baseline+p2) /2)*(1-((baseline+p2) /2))
    n = s * ((zp + z)**2) / (MDE**2)

    sampleSize = int(round(n[0]))

    return fig, sampleSize

if __name__ == "__main__":
    app.run_server(debug=False, port = 8050)