import pandas as pd
import plotly.graph_objects as go
import numpy as np
import scipy.stats as st

import os

# Bio needs to be installed by the user,
# can be done with conda install biopython
from Bio import SeqIO

# gzip needs to also be installed by the user,
# can be done with conda install gzip
import gzip

def quality_hist():
    directory = 'data/exported_demux/'
    filename = 'per-sample-fastq-counts.tsv'
    reads_per = pd.read_csv(directory+filename, sep='\t')
    reads_per_hist = go.Figure(data=[go.Histogram(x=reads_per['forward sequence count'], nbinsx=reads_per.shape[0])])
    reads_per_hist.update_layout(
    title_text='Histogram of reads per sample', # title of plot
    xaxis_title_text='Number of sequences', # xaxis label
    yaxis_title_text='Number of samples', # yaxis label
    )
    return reads_per_hist

def get_scores(filename, depth):
    """Inner most function for quality score plotting, makes a record
    of the quality scores in a given fastq file and creates a
    dataframe of the resulting scores by position for n = depth
    reads"""
    if filename.endswith('.gz'):
        fastq_parser = SeqIO.parse(gzip.open(filename, "rt"),
                                   "fastq")
        result = []
        count = 0
        for record in fastq_parser:
            score = record.letter_annotations["phred_quality"]
            count += 1
            result.append(score)
            if count > depth:
                break
        sample_scores = pd.DataFrame(result)
        return sample_scores
    elif filename.endswith('.fastq'):
        fastq_parser = SeqIO.parse(filename, "fastq")
        result = []
        count = 0
        for record in fastq_parser:
            score = record.letter_annotations["phred_quality"]
            count += 1
            result.append(score)
            if count > depth:
                break
        sample_scores = pd.DataFrame(result)
        return sample_scores


def sum_scores(directory, depth):
    """Middle layer function that iterated through a directory
    given as a parameter. Calls the get_scores function on
    every file within the directory, appending the score dataframe
    to the existing dataframe of scores"""
    sum_df = pd.DataFrame()
    for file in os.listdir(directory):
        sample_scores = get_scores(directory+'/'+file, depth)
        sum_df = sum_df.append(sample_scores, ignore_index=True)
    read_pos = sum_df.columns.to_list()
    return read_pos, sum_df


def find_dropoff(directory, depth):
    """This function find the position in the reads at which the average phred
    quality score drops below a certain threshold. This is meant to inform the
    user at which base to trim their reads"""
    read_pos, sum_df = sum_scores(directory, depth)
    means = sum_df.mean()
    pos1 = next((position for position,
                 score in enumerate(means) if score < 30), None)
    pos2 = next((position for position,
                 score in enumerate(means) if score < 25), None)
    pos3 = next((position for position,
                 score in enumerate(means) if score < 20), None)
    pos4 = next((position for position,
                 score in enumerate(means) if score < 15), None) 
    print('\n',
          'Here is some information about the quality of your reads to help you choose a trim length\n',
          '\n',
          'the average quality of your reads drops below a phred score of 30 at position', pos1, '\n',
          'the average quality of your reads drops below a phred score of 25 at position', pos2, '\n',
          'the average quality of your reads drops below a phred score of 20 at position', pos3, '\n',
          'the average quality of your reads drops below a phred score of 15 at position', pos4, '\n')
    if pos1 == None:
        print('Your sequence quality scores are awesome throughout the whole length of your reads!', '\n',
              'Enter 0 for trim length to retain the entire length of your reads.')
    return


def plot_qualities(directory, depth):
    """This function takes a directory and a sampling depth as parameters
    and calls the sum_scores function to create dataframe with a sample
    of each fastq file quality scores, then generates a plotly object
    showing the mean quality score by position with error bars representing
    the 95% confidence intervals"""
    read_pos, sum_df = sum_scores(directory, depth)
    means = sum_df.mean()
    confidence = 0.90
    # calculating 95% CI for phred scores for plotting
    ci95_lo = []
    for column in sum_df:
        base_scores = sum_df[column]
        # t statistic 95% CI
        interval = st.t.interval(confidence, len(base_scores.values)-1,
                                 loc=np.mean(base_scores.values),
                                 scale=st.tstd(base_scores.values))
        # appending the lower CI intervals
        ci95_lo.append(interval[0])
    CI_below = []
    for num1, num2 in zip(ci95_lo, means):
        CI_below.append(np.abs(num1 - num2))
    CI_below = [x * 1.5 for x in CI_below]
    max_quality = []
    for column in sum_df:
        scores = sum_df[column]
        max_quality.append(np.max(scores.values))
    error_dict = dict(
        type='data',
        symmetric=False,
        color='black',
        thickness=1,
        array=max_quality-means,
        arrayminus=CI_below)
    # create figure object
    fig = go.Figure()
    # adding low quality score patch
    fig.add_trace(go.Scatter(x=[0, 0, len(read_pos), len(read_pos)],
                             y=[0, 20, 20, 0], fill='toself',
                             showlegend=False,
                             fillcolor='rgba(244, 0, 0,0.3)',
                             line_width=0, mode='none',
                             name='error highly likely'))
    # adding mid-quality score patch
    fig.add_trace(go.Scatter(x=[0, 0, len(read_pos), len(read_pos)],
                             y=[20, 28, 28, 20], fill='toself',
                             showlegend=False,
                             fillcolor='rgba(244, 122, 0,0.2)',
                             line_width=0, mode='none',
                             name='likely to contain an error'))
    # adding high quality score patch
    fig.add_trace(go.Scatter(x=[0, 0, len(read_pos), len(read_pos)],
                             y=[28, 40, 40, 28], fill='toself',
                             showlegend=False,
                             fillcolor='rgba(0, 244, 0,0.2)',
                             line_width=0, mode='none',
                             name='likely no error'))
    # plotting mean scores with error bars
    fig.add_trace(go.Scatter(x=read_pos, y=means,
                             mode='lines', showlegend=False,
                             error_y=error_dict, name='mean phred'))
    fig.update_layout(yaxis_range=[0, 40], xaxis_range=[0, len(read_pos)])
    fig.update_layout(title_text='Mean Phred Quality Scores by Position; ' + f'Sampling Depth = {depth}')
    fig.update_xaxes(title_text='Position (bp)')
    fig.update_yaxes(title_text='phred quality score')
    return fig


def plotly_stacked_barplot(df, plot_title):
    """Given a dataframe and a plot title, returns a plotly
    stacked barplot figure of the taxonomy data"""
    fig = go.Figure()

    for item, col in df.iteritems():
        fig.add_trace(go.Bar(name=item, x=col.index, y=col))

    fig.update_layout(barmode='stack')
    fig.update_layout(title_text=plot_title, title_x=0.33)
    fig.update_xaxes(title_text='Sample')
    fig.update_yaxes(title_text='Relative Frequency')
    return fig


def get_feature_info(filepath):
    """Given a feature table, will print stats on feature counts"""
    colnames = ['sample-id', 'num_features']
    features = pd.read_csv(filepath, skiprows=1, names=colnames)
    min_feats = np.min(features['num_features'].values).astype(int)
    max_feats = np.max(features['num_features'].values).astype(int)
    mean_feats = np.mean(features['num_features'].values).astype(int)
    stdev_feats = np.std(features['num_features'].values).astype(int)
    
    suggest = 0
    if min_feats <= 100:
        suggest = mean_feats - stdev_feats
    elif min_feats > 100:
        suggest = min_feats - 1
    
    print('\n',
          'Here is some information about the number of features in your samples:\n',
          '\n',
          'Minimum number of features:', min_feats, '\n',
          'Maximum number of features:', max_feats, '\n',
          'Mean number of features:', mean_feats, '\n',
          'Standard deviation of feature counts across samples:', stdev_feats, '\n',
          '\n',
          'We would suggest using a sampling depth of or below:', suggest)
    return