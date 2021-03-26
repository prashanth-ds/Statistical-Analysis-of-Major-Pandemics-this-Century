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


def total_cases_bar_chart(entry, title, legend):
    trace = go.Bar(name=entry.columns[0], x=entry.index, y=entry[entry.columns[0]], marker=dict(color='#999999'))

    layout = go.Layout(title=title,
                       xaxis=go.layout.XAxis(
                           title='Countries',
                           showticklabels=False
                       ),
                       yaxis=go.layout.YAxis(
                           title=entry.columns[0]
                       ),
                       hovermode='x'
                       )

    fig = go.Figure(data=[trace], layout=layout)

    return plot(fig,
                output_type='div')
