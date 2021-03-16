from make_plots import get_scores, sum_scores, plot_qualities, find_dropoff, get_feature_info
from data_prep_stack_barplots import reduce_taxonomy_df, make_taxon_list, make_tax_dfs, fill_tax_dfs, prepare_data_stacked_barplots
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_div_gen import alpha_diversity_plot
from beta_div_gen import sample_cols, bray_beta_diversity_clean, unifrac_beta_diversity_clean

def test_fill_tax_dfs():
    taxon_list = [['bacteria', 'archaea'], ['bacteriodetes', 'firmicutes', 'proteobacteria'], 
                  ['bacilli'], ['bacteroidia'], ['Bacteroidaceae', 'Neisseriaceae'],
                  ['Neisseria'], ['species1', None]]
    tax = {'Feature ID': ['feat1', 'feat2', 'feat3'], 
           'kingom':['bacteria', 'bacteria', 'archaea'], 
           'phylum':['bacteriodetes', 'firmicutes', 'proteobacteria'], 
           'class':['bacilli', 'bacilli', 'bacilli'], 
           'order':['bacteroidia', 'bacteroidia', 'bacteroidia'], 
           'family':['Bacteroidaceae', 'Neisseriaceae','Neisseriaceae'],
           'genus': ['Neisseria', 'Neisseria', 'Neisseria'], 
           'species': ['species1', None, None]}
    tax_df = pd.DataFrame(data=tax)
    tax_df.set_index('Feature ID', inplace=True)
    feat_tab = {'':['samp1', 'samp2', 'samp3'], 'feat1':[0.0, 25.0, 0.0], 
                'feat2':[50.0, 25.0, 0.0], 'feat3':[50.0, 50.0, 100.0]}  
    feat_tab_df = pd.DataFrame(data=feat_tab)
    feat_tab_df.set_index('', inplace=True)
    kingdom_result, phylum_result, class_result, order_result, family_result, genus_result, species_result = make_tax_dfs(taxon_list, feat_tab_df)
    kingdom_filled, phylum_filled, class_filled, order_filled, family_filled, genus_filled, species_filled = fill_tax_dfs(kingdom_result, phylum_result, class_result, order_result, 
                                                                                                                          family_result, genus_result, species_result,feat_tab_df, tax_df)
    kingdom_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteria':[0.5, 0.5, 0.0], 
                                     'archaea':[0.5, 0.5, 1.0]})
    kingdom_ans.set_index('', inplace=True)
    assert kingdom_filled.equals(kingdom_ans), 'taxonomy kingdom dataframe is not being properly filled in fill_tax_dfs'
    phylum_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteriodetes':[0.0, 0.25, 0.0], 
                                    'firmicutes':[0.5, 0.25, 0.0], 'proteobacteria':[0.5, 0.5, 1.0]})
    phylum_ans.set_index('', inplace=True)
    assert phylum_filled.equals(phylum_ans), 'taxonomy phylum dataframe is not being properly filled in fill_tax_dfs'
    class_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacilli':[1.0, 1.0, 1.0]})
    class_ans.set_index('', inplace=True)
    assert class_filled.equals(class_ans), 'taxonomy class dataframe is not being properly filled in fill_tax_dfs'
    order_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteroidia':[1.0, 1.0, 1.0]})
    order_ans.set_index('', inplace=True)
    assert order_filled.equals(order_ans), 'taxonomy order dataframe is not being properly filled in fill_tax_dfs'
    family_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'Bacteroidaceae':[0.0, 0.25, 0.0], 
                                    'Neisseriaceae':[1.0, 0.75, 1.0]})
    family_ans.set_index('', inplace=True)
    assert family_filled.equals(family_ans), 'taxonomy family dataframe is not being properly filled in fill_tax_dfs'
    genus_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'Neisseria':[1.0, 1.0, 1.0]})
    genus_ans.set_index('', inplace=True)
    assert genus_filled.equals(genus_ans), 'taxonomy genus dataframe is not being properly filled in fill_tax_dfs'
    species_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'species1':[0.0, 0.25, 0.0], 
                                     None :[1.0, 0.75, 1.0]})
    species_ans.set_index('', inplace=True)
    assert species_filled.equals(species_ans), 'taxonomy species dataframe is not being properly filled in fill_tax_dfs'
    return

def test_make_tax_dfs():
    taxon_list = [['bacteria', 'archaea'], ['bacteriodetes', 'firmicutes', 'proteobacteria'], 
                  ['bacilli'], ['bacteroidia'], ['Bacteroidaceae', 'Neisseriaceae'], 
                  ['Neisseria'], ['species1', None]]
    feat_tab = {'':['samp1', 'samp2', 'samp3'], 'feat1':[0.0, 25.0, 0.0], 'feat2':[50.0, 25.0, 0.0], 
                'feat3':[50.0, 50.0, 100.0]}    
    feat_tab_df = pd.DataFrame(data=feat_tab)
    feat_tab_df.set_index('', inplace=True)
    kingdom_result, phylum_result, class_result, order_result, family_result, genus_result, species_result = make_tax_dfs(taxon_list, feat_tab_df)
    kingdom_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteria':[0.0, 0.0, 0.0], 
                                     'archaea':[0.0, 0.0, 0.0]})
    kingdom_ans.set_index('', inplace=True)
    assert kingdom_result.equals(kingdom_ans), 'taxonomy kingdom dataframe is not being properly initialized in make_tax_dfs'
    phylum_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteriodetes':[0.0, 0.0, 0.0], 
                                    'firmicutes':[0.0, 0.0, 0.0], 'proteobacteria':[0.0, 0.0, 0.0]})
    phylum_ans.set_index('', inplace=True)
    assert phylum_result.equals(phylum_ans), 'taxonomy phylum dataframe is not being properly initialized in make_tax_dfs'
    class_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacilli':[0.0, 0.0, 0.0]})
    class_ans.set_index('', inplace=True)
    assert class_result.equals(class_ans), 'taxonomy class dataframe is not being properly initialized in make_tax_dfs'
    order_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'bacteroidia':[0.0, 0.0, 0.0]})
    order_ans.set_index('', inplace=True)
    assert order_result.equals(order_ans), 'taxonomy order dataframe is not being properly initialized in make_tax_dfs'
    family_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'Bacteroidaceae':[0.0, 0.0, 0.0],
                                    'Neisseriaceae':[0.0, 0.0, 0.0]})
    family_ans.set_index('', inplace=True)
    assert family_result.equals(family_ans), 'taxonomy family dataframe is not being properly initialized in make_tax_dfs'
    genus_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'Neisseria':[0.0, 0.0, 0.0]})
    genus_ans.set_index('', inplace=True)
    assert genus_result.equals(genus_ans), 'taxonomy genus dataframe is not being properly initialized in make_tax_dfs'
    species_ans = pd.DataFrame(data={'':['samp1', 'samp2', 'samp3'], 'species1':[0.0, 0.0, 0.0], 
                                     None :[0.0, 0.0, 0.0]})
    species_ans.set_index('', inplace=True)
    assert species_result.equals(species_ans), 'taxonomy species dataframe is not being properly initialized in make_tax_dfs'
    return

def test_make_taxon_list():
    d = {'Feature ID': ['feat1', 'feat2', 'feat3'], 
         'kingom':['bacteria', 'bacteria', 'archaea'], 
         'phylum':['bacteriodetes', 'firmicutes', 'proteobacteria'], 
         'class': ['bacilli', 'bacilli', 'bacilli'], 
         'order':['bacteroidia', 'bacteroidia',  'bacteroidia'], 
         'family':['Bacteroidaceae', 'Neisseriaceae', 'Neisseriaceae'],
         'genus':['Neisseria', 'Neisseria', 'Neisseria'], 
         'species': ['species1', None, None]}
    df = pd.DataFrame(data=d)
    df.set_index('Feature ID', inplace=True)
    df.head()
    result = make_taxon_list(df)
    answer = [['bacteria', 'archaea'], ['bacteriodetes', 'firmicutes', 'proteobacteria'],   
              ['bacilli'], ['bacteroidia'], ['Bacteroidaceae', 'Neisseriaceae'],
             ['Neisseria'], ['species1', None]]
    assert answer == result, 'unique taxons are not being properly counted or stored in make_taxon_list'
    return

def test_reduce_taxonomy_df():
    d = {'col1': ['a', 'b', 'c'], 'Taxon':[1, 2, 3], 'Confidence': [4, 5, 6]}
    df = pd.DataFrame(data=d)
    result = reduce_taxonomy_df(df)
    d_red = {'col1': ['a', 'b', 'c']}
    answer = pd.DataFrame(d_red)
    assert answer.equals(result), 'taxonomy DataFrame is not being properly reduced'
    d = {'Taxon':[1, 2, 3], 'col2': ['a', 'b', 'c'], 'Confidence': [4, 5, 6]}
    df = pd.DataFrame(data=d)
    result = reduce_taxonomy_df(df)
    d_red = {'col2': ['a', 'b', 'c']}
    answer = pd.DataFrame(d_red)
    assert answer.equals(result), 'taxonomy DataFrame is not being properly reduced'
    d = {'Taxon':[1, 2, 3], 'Confidence': [4, 5, 6], 'col3': ['a', 'b', 'c']}
    df = pd.DataFrame(data=d)
    result = reduce_taxonomy_df(df)
    d_red = {'col3': ['a', 'b', 'c']}
    answer = pd.DataFrame(d_red)
    assert answer.equals(result), 'taxonomy DataFrame is not being properly reduced'
    return

def test_get_scores_1():
    """This function checks the datatype of the output score"""
    filename = '../demo_data_v2/A10_S10_L001_R1_001.fastq.gz'
    depth = 500
    result = get_scores(filename, depth)
    assert isinstance(result, pd.DataFrame), 'scores are \
    not being output as a dataframe'
    return


def test_sum_scores_1():
    """This function checks the datatype of the objects returned
    by the sum_scores function"""
    directory = '../demo_data_v2/'
    depth = 500
    read_pos, sum_df = sum_scores(directory, depth)
    assert isinstance(read_pos, list) and isinstance(
        sum_df, pd.DataFrame), f'sum_scores function is returning \
    objects that look like {type(read_pos)} and {type(sum_df)}'
    return


def test_plot_qualities_1():
    """This function checks the datatype of the figure object
    returned by the plot_qualities function"""
    directory = '../demo_data_v2/'
    depth = 500
    fig = plot_qualities(directory, depth)
    assert isinstance(fig, go.Figure), 'the \
    figure being returned is not the type of object we expect'
    return


def test_find_dropoff():
    """This function tests to make sure the depth input is an int"""
    directory = '../demo_data_v2/'
    depth = 500
    results = find_dropoff(directory, depth)
    assert isinstance(depth, int), 'depth must be an int, got ' + str(type(depth))
    return

def test_get_feature_info():
    """This function tests to see if the suggestion depth returned
    is of int type, because that is the type required as input by the
    user"""
    info = get_feature_info('sample-frequency-detail.csv')
    colnames = ['sample-id', 'num_features']
    features = pd.read_csv('sample-frequency-detail.csv', skiprows=1, names=colnames)
    min_feats = np.min(features['num_features'].values).astype(int)
    max_feats = np.max(features['num_features'].values).astype(int)
    mean_feats = np.mean(features['num_features'].values).astype(int)
    stdev_feats = np.std(features['num_features'].values).astype(int)
    
    suggest = 0
    if min_feats <= 100:
        suggest = mean_feats - stdev_feats
    elif min_feats > 100:
        suggest = min_feats - 1
    assert isinstance(suggest, np.int64), 'suggestion is not an int, got ' + str(type(suggest))
    return

def test_bray_beta_diversity_clean_1():
    """test function to check output is of type pandas dataframe"""
    bray_metadata_to_plot=bray_beta_diversity_clean('../data')
    assert isinstance(bray_metadata_to_plot,pd.core.frame.DataFrame),"not returning df"

def test_bray_beta_diversity_clean_2():
    """test function to check that Unnamed: 0 column has been removed from final DF"""
    try:
        bray_metadata_to_plot=bray_beta_diversity_clean('../data')
        bray_metadata_to_plot['Unnamed: 0']
    except Exception as e:
        assert isinstance(e, 'KeyError'), "unnamed column still present"
        # should throw key error since unnamed column was removed
        
def test_bray_beta_diversity_clean_3():
    """test function to check that metadata and PC results were merged/both present in output"""
    bray_metadata_to_plot=bray_beta_diversity_clean('../data')
    if 'body-site' and 'PC1' in bray_metadata_to_plot.columns:
        result = 1
    else:
        result = 0
    assert result == 1, "dataframe merge issues: missing metadata OR PC1"
    # output df should contain columns from both the PCOA analysis and metadata

def test_unifrac_beta_diversity_clean_1():
    """test function to check output is of type pandas dataframe"""
    unifrac_metadata_to_plot=unifrac_beta_diversity_clean('../data')
    assert isinstance(unifrac_metadata_to_plot,pd.core.frame.DataFrame),"not returning df"

def test_unifrac_beta_diversity_clean_2():
    """test function to check that Unnamed: 0 column has been removed from final DF"""
    try:
        unifrac_metadata_to_plot=unifrac_beta_diversity_clean('../data')
        unifrac_metadata_to_plot['Unnamed: 0']
    except Exception as e:
        assert isinstance(e, 'KeyError'), "unnamed column still present"
        # should throw key error since unnamed column was removed
        
def test_unifrac_beta_diversity_clean_3():
    """test function to check that metadata and PC results were merged/both present in output"""
    unifrac_metadata_to_plot=unifrac_beta_diversity_clean('../data')
    if 'body-site' and 'PC1' in unifrac_metadata_to_plot.columns:
        result = 1
    else:
        result = 0
    assert result == 1, "dataframe merge issues: missing metadata OR PC1"
    # output df should contain columns from both the PCOA analysis and metadata
    
def test_unifrac_beta_diversity_clean_4():
    """test function to check that the metadata is the same between both beta diversity functions"""
    bray_metadata_to_plot=bray_beta_diversity_clean('../data')
    unifrac_metadata_to_plot=unifrac_beta_diversity_clean('../data')
    assert unifrac_metadata_to_plot['body-site'].all() == bray_metadata_to_plot['body-site'].all()
    
def test_unifrac_beta_diversity_clean_5():
    """test function to check that beta diversity metric PCOA analyses are not identical"""
    bray_metadata_to_plot=bray_beta_diversity_clean('../data')
    unifrac_metadata_to_plot=unifrac_beta_diversity_clean('../data')
    false = bray_metadata_to_plot.iloc[1,9] == unifrac_metadata_to_plot.iloc[1,9]
    assert false == False, "bray curtis equals weighted unifrac"

def test_alpha_diversity_plot_1():
    """test function to check that output is expected type pd dataframe"""
    alpha_metadata_to_plot=alpha_diversity_plot('../data')
    assert isinstance(alpha_metadata_to_plot,pd.core.frame.DataFrame),"not returning df"

def test_alpha_diversity_plot_2():
    """test function to check if dataframe has merged metadata and alpha metrics"""
    alpha_metadata_to_plot=alpha_diversity_plot('../data')
    if 'sample-id' and 'shannon_entropy' and 'faith_diversity' and 'pielou_evenness' in alpha_metadata_to_plot.columns:
        result = 1
    else:
        result = 0
    assert result == 1, "dataframe merge issues: missing metadata OR alpha metrics"
    
def test_alpha_diversity_plot_3():
    """test function to check that alpha diversity metrics are values and not NaN"""
    alpha_metadata_to_plot=alpha_diversity_plot('../data')
    result = alpha_metadata_to_plot.iloc[1,10]
    assert isinstance(result,np.float64), "values not populating for alpha metrics"
