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
import alpha_div_gen
import beta_div_gen

# Summary statistics file import and processing for callback

basename = input('Name of visualization file:')

if ('.pkl' in basename):
    filename = basename
else:
    filename = basename + '.pkl'

with open(filename, 'rb') as f:
    king_plot, phy_plot, class_plot, ord_plot, fam_plot, gen_plot, spec_plot, qual_plot, qual_hist = pickle.load(f)

fig_dict = {
    'fam': fam_plot,
    'gen': gen_plot,
    'king': king_plot,
    'ord': ord_plot,
    'phy': phy_plot,
    'spec': spec_plot,
    'class': class_plot,
}

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
            {'label': 'Family', 'value': 'fam'},
            {'label': 'Genus', 'value': 'gen'},
            {'label': 'Kingdom', 'value': 'king'},
            {'label': 'Order', 'value': 'ord'},
            {'label': 'Phylum', 'value': 'phy'},
            {'label': 'Species', 'value': 'spec'},
            {'label': 'Class', 'value': 'class'}
        ],
        value='fam' # Default value upon startup
    ),
    
    dcc.Graph(id='selected_plot')
])

summary_page = html.Div([
    dcc.Graph(figure=qual_plot),
    dcc.Graph(figure=qual_hist)
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
                 for x in ['shannon_entropy','faith_diversity','pielou_evenness','observed_features']],
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
    return fig_dict[figure_name]

@app.callback(
    dash.dependencies.Output("alpha-plot", "figure"), 
    [dash.dependencies.Input("x-axis", "value"), 
     dash.dependencies.Input("y-axis", "value")])
def generate_alpha_chart(x, y):
    fig = px.box(df, x=x, y=y)
    return fig

@app.callback(
    dash.dependencies.Output("beta-plot", "figure"), 
    [dash.dependencies.Input("beta_type", "value"),
     dash.dependencies.Input('meta-col', 'value')])
def generate_beta_chart(beta_type, meta_col):
    df = beta_dict[beta_type]
    fig = px.scatter_3d(df, x='PC1', y='PC2', z='PC3', color=meta_col)
    return fig

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8050', debug=False)
