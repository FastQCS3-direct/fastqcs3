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
        sample_scores = get_scores(str(directory+file), depth)
        sum_df = sum_df.append(sample_scores, ignore_index=True)
    read_pos = sum_df.columns.to_list()
    return read_pos, sum_df


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
