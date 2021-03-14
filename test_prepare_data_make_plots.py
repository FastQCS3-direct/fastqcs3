from make_plots import get_scores, sum_scores, plot_qualities, find_dropoff
from data_prep_stack_barplots import reduce_taxonomy_df, make_taxon_list, make_tax_dfs, fill_tax_dfs, prepare_data_stacked_barplots
import pandas as pd
import plotly.graph_objects as go

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
    filename = '../jdm_sample_seqs/12_S12_L001_R1_001.fastq.gz'
    depth = 1000
    result = get_scores(filename, depth)
    assert isinstance(result, pd.DataFrame), 'scores are \
    not being output as a dataframe'
    return


def test_sum_scores_1():
    """This function checks the datatype of the objects returned
    by the sum_scores function"""
    directory = '../jdm_sample_seqs/'
    depth = 1000
    read_pos, sum_df = sum_scores(directory, depth)
    assert isinstance(read_pos, list) and isinstance(
        sum_df, pd.DataFrame), f'sum_scores function is returning \
    objects that look like {type(read_pos)} and {type(sum_df)}'
    return


def test_plot_qualities_1():
    """This function checks the datatype of the figure object
    returned by the plot_qualities function"""
    directory = '../jdm_sample_seqs/'
    depth = 1000
    fig = plot_qualities(directory, depth)
    assert isinstance(fig, go.Figure), 'the \
    figure being returned is not the type of object we expect'
    return


def test_find_dropoff():
    directory = '/Users/evanpepper/Desktop/exported-demux/'
    depth = 50
    results = find_dropoff(directory, depth)
    assert isinstance(depth, int), 'depth must be an int, got ' + str(type(depth))
    return
