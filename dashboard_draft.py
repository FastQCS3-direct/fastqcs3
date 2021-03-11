# -*- coding: utf-8 -*-

# Run this app with `python dashboard_draft.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Holy fuck this works??'),
    
    dcc.Dropdown(
        id='data_selector',
        options=[
            {'label': 'family', 'value': 'family'},
            {'label': 'genus', 'value': 'genus'},
            {'label': 'kingdom', 'value': 'kingdom'},
            {'label': 'order', 'value': 'order'},
            {'label': 'phylum', 'value': 'phylum'},
            {'label': 'species', 'value': 'species'}
        ],
        value='kingdom' # Default value upon startup
    ),

    html.Div(children='''
        Seriously I don't know how this worked
    '''),

    dcc.Graph(id='barplot')
])

@app.callback(
    dash.dependencies.Output('barplot', 'figure'),
    [dash.dependencies.Input('data_selector', 'value')])
def update_graph(figure_name):
    read_name = figure_name + '.csv' # Adding .csv tail to input filename string
    base_path = '/home/nguyencd296/project/fastqcs3/csv_files/' # Modify this for your own path up to /fastqcs3
    read_path = base_path + read_name # Generating final path to access csv_files folder
    df = pd.read_csv(read_path) # index_col=0
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Removing any unnamed columns
    ylist = list(df.columns) # Generate list for column names
    ylist.pop(0) # Removing index column from column name list
    fig = px.bar(df, x='index', y=ylist)
    return fig

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=True)
