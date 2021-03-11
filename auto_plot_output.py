import subprocess
import make_plots
import data_prep_stack_barplots as prep
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

samp_depth = input("Desired sampling depth:")
if samp_depth.isdigit():
    pass
else:
    raise TypeError('sampling depth must be a positive integer')

"""runs auto_qiime function"""
auto_qiime(directory,trimlength)

"""read in newly created taxonomy AND FEATURE TABLE data file to pandas"""
taxonomy = pd.read_csv("data/taxonomy.tsv", sep='\t')
taxonomy[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = taxonomy['Taxon'].str.split(';', expand=True)
taxonomy.set_index('Feature ID', inplace=True)
# also get table working here and whatever kaylyn uses for her stuff

"""pre process data for relative abundance stacked bar plots"""
kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df = prep.prepare_data_stacked_barplots(t, tax)

"""create plotly figures"""
king_plot = make_plots.plotly_stacked_barplot(kingdom_df, 'Kingdom Relative Abundances')
phy_plot = make_plots.plotly_stacked_barplot(phylum_df, 'Phylum Relative Abundances')
class_plot = make_plots.plotly_stacked_barplot(class_df, 'Class Relative Abundances')
ord_plot = make_plots.plotly_stacked_barplot(order_df, 'Order Relative Abundances')
fam_plot = make_plots.plotly_stacked_barplot(family_df, 'Family Relative Abundances')
gen_plot = make_plots.plotly_stacked_barplot(genus_df, 'Genus Relative Abundances')
spec_plot = make_plots.plotly_stacked_barplot(species_df, 'Species Relative Abundances')

qual_plot = make_plots.plot_qualities(directory, samp_depth)

"""create dash layout"""
