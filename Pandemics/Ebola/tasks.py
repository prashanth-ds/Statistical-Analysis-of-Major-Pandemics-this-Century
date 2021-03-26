import plotly.graph_objs as go
from plotly.offline import *


def world_map(entry, title, legend):
    data_for_map = dict(type='choropleth',
                        locations=entry['Code'],
                        z=entry[entry.columns[0]],
                        colorscale='rainbow',
                        text=entry.index,
                        colorbar=dict(title=legend))

    layout = dict(title=title,
                  geo=dict(showframe=False,
                           projection_type='natural earth'))

    fig = go.Figure(data=[data_for_map], layout=layout)

    return plot(fig,
                output_type='div')


def bar_chart(entry, title):

    trace1 = go.Bar(name=entry.columns[1], x=entry['Country'], y=entry['Total Cases'], marker_color='#FE8B4E')
    trace2 = go.Bar(name=entry.columns[2], x=entry['Country'], y=entry['Total Deaths'], marker_color='red')

    layout = go.Layout(title=title,
                       barmode='group',
                       xaxis=go.layout.XAxis(
                           title='Countries',
                           showticklabels=False
                       ),
                       yaxis=go.layout.YAxis(
                           title=title
                       ),
                       hovermode='x'
                       )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return plot(fig,
                output_type='div')

