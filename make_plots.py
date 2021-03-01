import pandas as pd
import plotly.graph_objects as go

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
