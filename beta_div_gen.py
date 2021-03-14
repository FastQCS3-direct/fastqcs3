# Import libraries
import pandas as pd
from skbio.stats.ordination import pcoa
import plotly.express as px
import os

def bray_beta_diversity_clean(directory):
    """function that cleans data and generates final data frame for bray-curtis pcoa beta diversity plots"""
    
    # Load and clean metadata
    metadata = pd.read_csv(directory+'/metadata.tsv', sep='\t')
    metadata = metadata.drop(metadata.index[0])
    metadata = metadata.reset_index(drop=True)
    
    # Bray Curtis
    bray = pd.read_csv(directory+'/bray-distance-matrix.tsv', sep='\t', index_col=0)
    bray_different_index = pd.read_csv(directory+'/bray-distance-matrix.tsv', sep='\t')
    bray_distance_matrix = bray.rename_axis('sample-id', axis="columns")
    
    # PCOA Analysis and result matrix
    bray_pcoa = pcoa(bray_distance_matrix);
    bray_final_results = bray_pcoa.samples
    bray_final_results = bray_final_results.reset_index()
    
    # Cleaning sample ids to join to result matrix
    bray_sample_id = bray_different_index[['Unnamed: 0']]
    bray_sample_id = bray_sample_id.rename(columns={'Unnamed: 0':'sample-id'})
    bray_sample_id = bray_sample_id.reset_index()
    
    # Constructing final matrix with PCoA results AND metadata
    bray_pcoa_results = bray_sample_id.join(bray_final_results, on='index', lsuffix='l',rsuffix='r')
    bray_pcoa_results = bray_pcoa_results.drop(labels = ['indexl','indexr'],axis=1)
    bray_metadata_to_plot = metadata.merge(bray_pcoa_results,how='outer')
    return bray_metadata_to_plot

def unifrac_beta_diversity_clean(directory):
    """function that cleans data and generates final data frame for weighted unifrac pcoa beta diversity plots"""
    
    # Load and clean metadata
    metadata = pd.read_csv(directory+'/metadata.tsv', sep='\t')
    metadata = metadata.drop(metadata.index[0])
    metadata = metadata.reset_index(drop=True)
    
    # Weighted Unifrac
    unifrac = pd.read_csv(directory+'/unifrac_distance_matrix.tsv', sep='\t',index_col=0)
    unifrac_different_index = pd.read_csv(directory+'/unifrac_distance_matrix.tsv', sep='\t')
    unifrac_distance_matrix = unifrac.rename_axis('sample-id',axis='columns')
    
    # PCOA Analysis and result matrix
    unifrac_pcoa = pcoa(unifrac_distance_matrix);
    unifrac_final_results = unifrac_pcoa.samples
    unifrac_final_results = unifrac_final_results.reset_index()
    
    # Cleaning sample ids to join to result matrix
    unifrac_sample_id = unifrac_different_index[['Unnamed: 0']]
    unifrac_sample_id = unifrac_sample_id.rename(columns={'Unnamed: 0':'sample-id'})
    unifrac_sample_id = unifrac_sample_id.reset_index()
    
    # Constructing final matrix with PCoA Results AND metadata
    unifrac_pcoa_results = unifrac_sample_id.join(unifrac_final_results, on='index', lsuffix='l',rsuffix='r')
    unifrac_pcoa_results = unifrac_pcoa_results.drop(labels = ['indexl','indexr'],axis=1)
    unifrac_metadata_to_plot = metadata.merge(unifrac_pcoa_results,how='outer')
    return unifrac_metadata_to_plot