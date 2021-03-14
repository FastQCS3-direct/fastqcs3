# Import Libraries
import pandas as pd
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#directory = input('Please input the directory of your alpha diversity metrics:')

def alpha_diversity_plot(directory):
    """function that loads and cleans alpha diversity metrics into dataframe for use in dash boxplot"""
    # Loading and cleaning alpha diversity metrics
    shannon = pd.read_csv(directory+'/shannon-alpha-diversity.tsv', sep='\t')
    shannon.columns = ['sample-id','shannon_entropy']

    faith = pd.read_csv(directory+'/faith-alpha-diversity.tsv', sep='\t')
    faith.columns = ['sample-id','faith_diversity']

    pielou = pd.read_csv(directory+'/pielou-alpha-diversity.tsv', sep='\t')
    pielou.columns = ['sample-id','pielou_evenness']

    observed = pd.read_csv(directory+'/observed-features-alpha-diversity.tsv', sep='\t')
    observed.columns = ['sample-id','observed_features']
    
    # Load metadata from QIIME2 and append diversity metrics
    alpha_metadata = pd.read_csv(directory+'/metadata.tsv', sep='\t')
    alpha_metadata = alpha_metadata.drop(alpha_metadata.index[0])
    alpha_metadata = alpha_metadata.reset_index(drop=True)
    alpha_metadata = alpha_metadata.merge(shannon,how='outer')
    alpha_metadata = alpha_metadata.merge(faith,how='outer')
    alpha_metadata = alpha_metadata.merge(pielou,how='outer')
    alpha_metadata = alpha_metadata.merge(observed,how='outer')
    return alpha_metadata