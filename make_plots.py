import pandas as pd
import plotly.graph_objects as go

import os
import math
import pylab as plt
import matplotlib.patches as patches

# Bio needs to be installed by the user, can be done with conda install biopython
import Bio
from Bio import SeqIO

# gzip needs to also be installed by the user, can be done with conda install gzip
import gzip

import matplotlib
%matplotlib inline
matplotlib.rcParams.update({'font.size': 18})


# function for plotting quality scores by position of each read within a sample ie. 1_S1_L001_R1_001.fastq.gz

def plot_fastq_qualities(filename, ax=None, limit=10000):
    """This is the function for creating the plot, sampling 10000 reads from the file and plotting only the subset
    This is convenient because often times, the fastq files have a ton of reads, but we don't need all of them
    to get a general idea of how good the plot actually is
    """
    # creating a parser to read the gzipped file
    fastq_parser = SeqIO.parse(gzip.open(filename, "rt"), "fastq")
    res=[]
    c=0
    for record in fastq_parser:
        score=record.letter_annotations["phred_quality"]
        res.append(score)
        c+=1
        if c>limit:
            break
    df = pd.DataFrame(res)
    l = len(df.T)+1

    if ax==None:
        f,ax=plt.subplots(figsize=(12,5))
    rect = patches.Rectangle((0,0),l,20,linewidth=0,facecolor='r',alpha=.4)
    ax.add_patch(rect)
    rect = patches.Rectangle((0,20),l,8,linewidth=0,facecolor='yellow',alpha=.4)
    ax.add_patch(rect)
    rect = patches.Rectangle((0,28),l,12,linewidth=0,facecolor='g',alpha=.4)
    ax.add_patch(rect)
    df.mean().plot(ax=ax,c='black')
    boxprops = dict(linestyle='-', linewidth=1, color='black')
    df.plot(kind='box', ax=ax, grid=False, showfliers=False,
            color=dict(boxes='black',whiskers='black')  )
    ax.set_xticks(np.arange(0, l, 5))
    ax.set_xticklabels(np.arange(0, l, 5), fontsize=10)
    ax.set_xlabel('position(bp)')
    ax.set_xlim((0,l))
    ax.set_ylim((0,40))
    ax.set_title('per base sequence quality')    
    return



def plotly_stacked_barplot(df, plot_title):
    """Given a dataframe and a plot title, returns a plotly stacked barplot figure of the taxonomy data"""
    fig = go.Figure()

    for item, col in df.iteritems():
        fig.add_trace(go.Bar(name=item, x=col.index, y=col))

    fig.update_layout(barmode='stack')
    fig.update_layout(title_text=plot_title, title_x=0.33)
    fig.update_xaxes(title_text='Sample')
    fig.update_yaxes(title_text='Relative Frequency')
    return fig
