import dash
import dash_core_components as dcc
import dash_html_components as html

import pickle

import subprocess
import make_plots
import data_prep_stack_barplots as prep
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from qiime2.plugins import feature_table
from qiime2 import Artifact

def auto_qiime(directory,trimlength):
    """function to run auto qiime2 bash script, outputs data in appropriate form to work with for plotting"""
    subprocess.run(['bash','-c','bash auto_qiime.sh '+directory+' '+trimlength])

"""takes inputs of directory of .fastq files, trim length, and sampling depth for running the auto qiime script and creating quality plots"""
directory=input('Directory of .fastq files:')
trimlength=input('Sequencing trim length:')
if trimlength.isdigit():
    pass
else:
    raise TypeError('trim length input must be a positive integer')

samp_depth = input("sampling depth:")
if samp_depth.isdigit():
    samp_depth = int(samp_depth)
else:
    raise TypeError('sampling depth must be a positive integer')
    
basename = input('Please input your filename:')

if (' ' in basename):
    raise TypeError('Cannot have spaces in filename')
elif ('.' in basename):
    raise TypeError('Please avoid periods in filename to avoid file type confusion')
    
"""runs auto_qiime function"""
auto_qiime(directory,trimlength)

"""read in newly created taxonomy data file to pandas"""
taxonomy = pd.read_csv("data/taxonomy.tsv", sep='\t')
taxonomy[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = taxonomy['Taxon'].str.split(';', expand=True)
taxonomy.set_index('Feature ID', inplace=True)
taxonomy.shape

"""reads in table.qza file from qiime2 into DataFrame"""
unrarefied_table = Artifact.load('outputs/table.qza')
rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
rarefied_table = rarefy_result.rarefied_table
table = rarefied_table.view(pd.DataFrame)

# add in any other data structures that need to be read in

"""pre process data into dataframes for plotting taxonomy relative abundances in stacked barplots"""
kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df = prep.prepare_data_stacked_barplots(table, taxonomy)

"""create plotly figures"""
king_plot = make_plots.plotly_stacked_barplot(kingdom_df, 'Kingdom Relative Abundances')
phy_plot = make_plots.plotly_stacked_barplot(phylum_df, 'Phylum Relative Abundances')
class_plot = make_plots.plotly_stacked_barplot(class_df, 'Class Relative Abundances')
ord_plot = make_plots.plotly_stacked_barplot(order_df, 'Order Relative Abundances')
fam_plot = make_plots.plotly_stacked_barplot(family_df, 'Family Relative Abundances')
gen_plot = make_plots.plotly_stacked_barplot(genus_df, 'Genus Relative Abundances')
spec_plot = make_plots.plotly_stacked_barplot(species_df, 'Species Relative Abundances')
qual_plot = make_plots.plot_qualities(directory, samp_depth)
qual_hist = make_plots.quality_hist()

# Loading all plot files into a pkl file

filename = basename + '.pkl'

with open(filename, 'wb') as f:
    pickle.dump([king_plot, phy_plot, class_plot, ord_plot, fam_plot, gen_plot, spec_plot, qual_plot, qual_hist], f)