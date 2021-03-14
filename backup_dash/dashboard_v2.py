# -*- coding: utf-8 -*-

# Run this app with `python dashboard_draft.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle

basename = input('Please input the plotting files you would like to visualize:')

if ('.pkl' in basename):
    filename = basename
else:
    filename = basename + '.pkl'

with open(filename, 'rb') as f:
    king_plot, phy_plot, class_plot, ord_plot, fam_plot, gen_plot, spec_plot, qual_plot = pickle.load(f)

fig_dict = {
    'fam': fam_plot,
    'gen': gen_plot,
    'king': king_plot,
    'ord': ord_plot,
    'phy': phy_plot,
    'spec': spec_plot,
    'class': class_plot,
    'qual': qual_plot
}
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='fastQCS3: Data Processing and Visualization'),
    
    dcc.Dropdown(
        id='data_selector',
        options=[
            {'label': 'plot quality', 'value': 'qual'},
            {'label': 'family', 'value': 'fam'},
            {'label': 'genus', 'value': 'gen'},
            {'label': 'kingdom', 'value': 'king'},
            {'label': 'order', 'value': 'ord'},
            {'label': 'phylum', 'value': 'phy'},
            {'label': 'species', 'value': 'spec'},
            {'label': 'class', 'value': 'class'}
        ],
        value='qual' # Default value upon startup
    ),

    html.Div(children='''
        Created by: Nick Bohmann, Cassandra Maranas, Evan Pepper, Kaylyn Torkelson, Ben Nguyen
    '''),

    dcc.Graph(id='selected_plot')
])

@app.callback(
    dash.dependencies.Output('selected_plot', 'figure'),
    [dash.dependencies.Input('data_selector', 'value')])
def update_graph(figure_name):
    return fig_dict[figure_name]

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=False)
