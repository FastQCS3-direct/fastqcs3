# -*- coding: utf-8 -*-

# Run this app with `python dashboard_draft.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pickle
import warnings

import pandas as pd

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from py_files import alpha_div_gen
from py_files import beta_div_gen

# suppressing warning messages
warnings.filterwarnings("ignore")

# Summary statistics file import and processing for callback

basename = input('\nPlease enter the name you gave your visualization file:')

if '.pkl' in basename:
    filename = basename
else:
    filename = basename + '.pkl'

print('\n',
      'Copy the URL where Dash is running into your browser!',
      '\n')

with open(filename, 'rb') as f:
    king_plot, phy_plot, class_plot, ord_plot, fam_plot, gen_plot, spec_plot, qual_plot, qual_hist = pickle.load(
        f)

fig_dict = {
    'fam': fam_plot,
    'gen': gen_plot,
    'king': king_plot,
    'ord': ord_plot,
    'phy': phy_plot,
    'spec': spec_plot,
    'class': class_plot,
}

directory_2 = 'data/exported_demux'
filename_2 = '/per-sample-fastq-counts.tsv'
reads_per = pd.read_csv(directory_2 + filename_2, sep='\t')

# Generating data for Alpha diversity

df = alpha_div_gen.alpha_diversity_plot('data')

# Generating data for Beta diversity

beta_cols = beta_div_gen.sample_cols('data')
bray = beta_div_gen.bray_beta_diversity_clean('data')
unifrac = beta_div_gen.unifrac_beta_diversity_clean('data')

beta_dict = {
    'bray': bray,
    'unifrac': unifrac
}

# Defines pages for summary stats and Alpha diversity

taxonomy_page = html.Div([
    dcc.Dropdown(
        id='data_selector',
        options=[
            {'label': 'Kingdom', 'value': 'king'},
            {'label': 'Phylum', 'value': 'phy'},
            {'label': 'Class', 'value': 'class'},
            {'label': 'Order', 'value': 'ord'},
            {'label': 'Family', 'value': 'fam'},
            {'label': 'Genus', 'value': 'gen'},
            {'label': 'Species', 'value': 'spec'},

        ],
        value='fam'  # Default value upon startup
    ),

    dcc.Graph(id='selected_plot')
])

summary_page = html.Div([
    dcc.Graph(figure=qual_plot),
    dcc.Graph(figure=qual_hist),
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
])

alpha_page = html.Div([
    html.P("Subject Attributes (x-axis)"),
    dcc.Dropdown(
        id='x-axis',
        options=[{'value': x, 'label': x}
                 for x in df.columns],
        value='subject'
    ),
    html.P("Alpha Diversity metric (y-axis)"),
    dcc.Dropdown(
        id='y-axis',
        options=[{'value': x, 'label': x}
                 for x in ['shannon_entropy', 'faith_diversity', 'pielou_evenness', 'observed_features']],
        value='shannon_entropy',
    ),
    dcc.Graph(id="alpha-plot"),
])

beta_page = html.Div([
    html.P("Subject Attributes"),
    dcc.Dropdown(id='meta-col',
                 options=[{'value': x, 'label': x}
                          for x in beta_cols],
                 value=beta_cols[0]
                 ),
    html.P("Beta Diversity metric:"),
    dcc.RadioItems(
        id='beta_type',
        options=[{'value': x, 'label': x}
                 for x in ['bray', 'unifrac']],
        value='bray',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="beta-plot"),
])

# Main Dash Area

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children=dcc.Markdown('**fastQCS3**: Data Processing and Visualization')),
    html.H2(children=dcc.Markdown('*Visualization module')),

    html.Div(children='''
        Created by: Nick Bohmann, Cassandra Maranas, Evan Pepper, Kaylyn Torkelson, Ben Nguyen
    '''),

    dcc.RadioItems(
        id='display-page',
        options=[{'label': 'Summary Statistics', 'value': 'summary'},
                 {'label': 'Taxonomy Statistics', 'value': 'taxonomy'},
                 {'label': 'Alpha Diversity Statistics', 'value': 'alpha'},
                 {'label': 'Beta Diversity Statistics', 'value': 'beta'}
                 ],
        value='summary',
    ),

    html.Div(id='page-content')
])

# Main callback components


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('display-page', 'value')])
def display_page(pathname):
    '''Displays the page based on the input of the display-page callback'''
    page_dict = {
        'summary': summary_page,
        'alpha': alpha_page,
        'beta': beta_page,
        'taxonomy': taxonomy_page
    }
    return page_dict[pathname]


@app.callback(
    dash.dependencies.Output('selected_plot', 'figure'),
    [dash.dependencies.Input('data_selector', 'value')])
def update_graph(figure_name):
    '''Updates the graphs in the taxonomy page based on data_selector
    callback'''
    return fig_dict[figure_name]


@app.callback(
    dash.dependencies.Output("alpha-plot", "figure"),
    [dash.dependencies.Input("x-axis", "value"),
     dash.dependencies.Input("y-axis", "value")])
def generate_alpha_chart(x, y):
    '''Generates Alpha Diversity chart in Alpha Diversity page'''
    fig = px.box(df, x=x, y=y)
    return fig


@app.callback(
    dash.dependencies.Output("beta-plot", "figure"),
    [dash.dependencies.Input("beta_type", "value"),
     dash.dependencies.Input('meta-col', 'value')])
def generate_beta_chart(beta_type, meta_col):
    '''Generates Beta Diversity chart in Beta Diversity page'''
    df = beta_dict[beta_type]
    fig = px.scatter_3d(df, x='PC1', y='PC2', z='PC3', color=meta_col)
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=False)
