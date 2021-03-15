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

# print statements for user intro to software
print('')
print('WELCOME TO fastQCS3! Before you begin:\n',
      '\n',
      '1. Please make sure your .fastq.gz files are in a directory.\n',
      '2. If your sequences are still multiplexed:',
      'make sure your barcodes.fastq.gz file lives in the same directory as your sequences.\n',
      '3. Make sure your metadata file is in your current working directory and,\n',
      '4. Make sure your metadata file is named "sample-metadata.tsv".\n')


demux_status = input('Are your fastq.gz sequence file(s) demultiplexed? (y/n):')
if demux_status == 'y' or 'n':
    pass
else:
    raise NameError('Please enter either y or n')

def import_demuxed_data(directory):
    """function to run importing of pre-demultiplexed reads"""
    subprocess.run(['bash','-c','bash shell_scripts/auto_import.sh '+directory])
    return

def auto_demux(directory):
    """function to run importing and demultiplexing (demux) of multiplexed reads"""
    subprocess.run(['bash','-c','bash shell_scripts/auto_demux.sh '+directory])
    return

def auto_dada2(trimlength):
    """function to run dada2"""
    subprocess.run(['bash','-c','bash shell_scripts/auto_dada2.sh '+trimlength])
    return

def auto_classify_phylo(sample_n_features):
    """function for classification, phylogenetic analysis, outputs data in appropriate form to work with for plotting"""
    subprocess.run(['bash','-c','bash shell_scripts/auto_classify_phylo.sh '+sample_n_features])
    return

# prompt user to input directory path
directory = input('Please enter the name of your directory of .fastq.gz files (note: sequence data must be gzipped):')
# adding error statements
if (' ' in directory):
    raise TypeError('Cannot have spaces in directory name')
elif ('.' in directory):
    raise TypeError('Please avoid periods in directory name to avoid confusion')
    
# calling importing functions based on user input
if demux_status == 'n':
    auto_demux(directory)
elif demux_status == 'y':
    import_demuxed_data(directory)

# calling find_dropoff function to print information about sequence quality by position
# so that the user can choose their trimlength logically
make_plots.find_dropoff('data/exported_demux/', 500)

# prompting user to input trim length
trimlength = input('\nPlease choose a sequencing trim length:')
# adding error statements
if trimlength.isdigit():
    pass
else:
    raise TypeError('trim length input must be a positive integer')
    
# this second block will run dada2 and the following few commands
print('\n...running dada2...this may take a few minutes...')
auto_dada2(trimlength)

# calling get_feature_info to get some information on feature counts
# to let the user choose sampling depth
make_plots.get_feature_info('data/features/sample-frequency-detail.csv')

# prompting user to input sampling depth
sample_n_features = input('\nPlease choose a sampling depth:')
# adding error statements
if sample_n_features.isdigit():
    pass
else:
    raise TypeError('sampling depth input must be a positive integer')
    
# calling auto_classify_phylo to run remainder of commands
auto_classify_phylo(sample_n_features)

print('\n',
      'fastQCS3 has finished processing your data! Congrats!')
    
# prompting user to name their .pkl file
basename = input('\nPlease give your visualization file a name:')
# adding error statements
if (' ' in basename):
    raise TypeError('Cannot have spaces in filename')
elif ('.' in basename):
    raise TypeError('Please avoid periods in filename to avoid file type confusion')

# everything below is for creating the plotting objects
"""read in newly created taxonomy data file to pandas"""
taxonomy = pd.read_csv("data/taxonomy.tsv", sep='\t')
taxonomy[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = taxonomy['Taxon'].str.split(';', expand=True)
taxonomy.set_index('Feature ID', inplace=True)
taxonomy.shape

"""reads in table.qza file from qiime2 into DataFrame"""
unrarefied_table = Artifact.load('outputs/table.qza')
# call some bash script here for stats output, then ask people for their decided sampling depth
# samp_depth = input('Whatchu decide for sampling depth')
rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100) # sampling_depth=samp_depth later?
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
qual_plot = make_plots.plot_qualities('data/exported_demux/', 500)
# qual_plot = make_plots.plot_qualities(directory, 500)
qual_hist = make_plots.quality_hist()

# Loading all plot files into a pkl file

filename = basename + '.pkl'

with open(filename, 'wb') as f:
    pickle.dump([king_plot, phy_plot, class_plot, ord_plot, fam_plot, gen_plot, spec_plot, qual_plot, qual_hist], f)
    
print('\n',
      'Now please run the following command to visualize your data in dash!\n',
      '\n',
      'python integrated_dashboard.py',
      '\n')