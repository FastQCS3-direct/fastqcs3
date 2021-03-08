from make_plots import get_scores, sum_scores, plot_qualities
# from make_plots import  plotly_stacked_barplot
import pandas as pd
import plotly.graph_objects as go


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
