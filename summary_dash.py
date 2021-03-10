import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objects as go
import numpy as np

import make_plots
from make_plots import get_scores, sum_scores, plot_qualities


directory = '../../../exported-demux/'
filename = 'per-sample-fastq-counts.tsv'
reads_per = pd.read_csv(directory+filename, sep='\t')


reads_per_hist = go.Figure(data=[go.Histogram(x=reads_per['forward sequence count'], nbinsx=reads_per.shape[0])])
reads_per_hist.update_layout(
    title_text='Histogram of reads per sample', # title of plot
    xaxis_title_text='Number of sequences', # xaxis label
    yaxis_title_text='Number of samples', # yaxis label
)


quality_plot = plot_qualities(directory, 500)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Sample Summaries'),

        html.Div(children='''
            Here is some information about the samples you provided.
        '''),

        dcc.Graph(
            id='reads-per-hist',
            figure=reads_per_hist
        ),  
    ]),
    # New Div for table of samples and read counts
    html.Div([
        
        html.Div(children='''
            Table of samples and their total read counts
        '''),
        
        dash_table.DataTable(
            id='reads-per-table',
            columns=[{"name": i, "id": i} for i in reads_per.columns],
            data=reads_per.to_dict('records'),
        ),  
    ]),
    
    # New Div for quality plot
    html.Div([
        
        dcc.Graph(
            id='quality-plot',
            figure=quality_plot
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
