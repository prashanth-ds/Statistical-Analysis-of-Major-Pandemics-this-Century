from . import worldo
from django.db import connection
import requests
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
import datetime
from Covid import who, india, india_testing, Automations


def check_connection(url):
    try:
        response = requests.head(url)
        print(response, "connection success")
        return True
    except requests.ConnectionError as e:
        print(e)
        return False


def write_world_daily():
    if check_connection('https://www.worldometers.info/coronavirus/'):
        worldo.call_collect()
        ret = worldo.enter_data()
        if ret is None:
            print('done entering in DB')
        else:
            print("No entry in DB")
    else:
        print('NO CONNECTION')


def automating():
    now = datetime.datetime.now().date()

    def automate():
        with connection.cursor() as cursor:
            query = 'SELECT * FROM pandemics.data_automation WHERE dates=%s;'
            cursor.execute(query, [now])
            data = cursor.fetchone()
            print(data)
            if data[2] == 0:
                Automations.who_country()  # Download the latest file from web
                who.enter()  # it takes nearly 100s to enter around 90,000 rows in DB with 9 columns in each row
                i = 1
            if data[3] == 0 or data[4] == 0:
                Automations.kagg()  # Download the latest file from web
                india.enter()  # it takes nearly 13s to enter around 9,000 rows in DB with 9 columns in each row
                india_testing.enter()  # it takes nearly 9s to enter around 8,000 rows in DB with 6 columns in each row
                j = 1
                k = 1
                # update_show(i, j, k)

    if check_connection("https://www.google.com/"):
        present_time = datetime.datetime.now().timetuple()
        if present_time[3] >= 12:
            automate()
    else:
        print("Will Update data once Network is available")


def line_chart(entry, columns, legend, color1='blue', color2='black', title='Linear', x_title='Countries'):
    lay_title = title
    entry = entry.iloc[::-1]
    if columns == 1:
        trace = go.Scatter(x=entry.index,
                           y=entry[entry.columns[0]],
                           mode='lines',
                           name='New Cases',
                           marker_color=color1,
                           )
        layout = go.Layout(title=lay_title,
                           xaxis=go.layout.XAxis(
                               title='Countries',
                               showticklabels=False
                           ),
                           yaxis=go.layout.YAxis(
                               title=entry.columns[0]
                           ),
                           showlegend=True,
                           hovermode='x'
                           )
        fig = go.Figure(data=[trace], layout=layout)
    if columns == 2:
        trace1 = go.Scatter(x=entry.index,
                            y=entry[entry.columns[0]],
                            mode='lines',
                            name=legend[0],
                            marker_color=color1,
                            )
        trace2 = go.Scatter(x=entry.index,
                            y=entry[entry.columns[1]],
                            mode='lines',
                            name=legend[1],
                            marker_color=color2,
                            )
        layout = go.Layout(title=lay_title,
                           xaxis=go.layout.XAxis(
                               title=x_title,
                               showticklabels=False
                           ),
                           yaxis=go.layout.YAxis(
                               title=str(entry.columns[0] + " & " + entry.columns[1])
                           ),
                           hovermode='x'
                           )
        fig = go.Figure(data=[trace1, trace2], layout=layout)

    return plot(fig,
                output_type='div')


def bar_chart(entry, legend, color='#999999', title='Bar'):
    lay_title = title
    entry.sort_index(inplace=True)
    trace = go.Bar(x=entry.index,
                   y=entry[entry.columns[0]],
                   name=legend[0],
                   marker=dict(color=color)
                   )

    layout = go.Layout(title=lay_title,
                       xaxis=go.layout.XAxis(
                           title='Countries',
                           showticklabels=False
                       ),
                       yaxis=go.layout.YAxis(
                           title=entry.columns[0]
                       ),
                       showlegend=True,
                       hovermode='x'
                       )
    fig = go.Figure(data=[trace], layout=layout)
    return plot(fig,
                output_type='div')


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


def india_map(entry):
    fig = px.choropleth(
        entry,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=entry.columns[0],
        locationmode='geojson-id',
        color=entry.columns[1],
        color_continuous_scale='Reds',
        title='Total Cases'
    )

    fig.update_geos(fitbounds="locations", visible=False)

    return plot(fig,
                output_type='div')


def line_chart_non_p(entry, legend, color1='blue', color2='black', title='Linear', x_title='Countries'):
    # print(entry.head())
    trace1 = go.Scatter(x=entry.index,
                        y=entry[entry.columns[0]],
                        mode='lines',
                        name=legend[0],
                        marker_color=color1,
                        )
    trace2 = go.Scatter(x=entry.index,
                        y=entry[entry.columns[1]],
                        mode='lines',
                        name=legend[1],
                        marker_color=color2,
                        )
    layout = go.Layout(title=title,
                       xaxis=go.layout.XAxis(
                           title=x_title,
                           showticklabels=False
                       ),
                       yaxis=go.layout.YAxis(
                           title=str(entry.columns[0] + " & " + entry.columns[1])
                       ),
                       hovermode='x'
                       )
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    return plot(fig,
                output_type='div')


def stacked_bar_graph(entry, legend, title):
    entry.sort_index(inplace=True)
    # print(entry)
    trace = go.Bar(x=entry.index,
                   y=entry[entry.columns[0]],
                   name=legend[0],
                   marker=dict(color='#FE8B4E')
                   )

    trace1 = go.Bar(x=entry.index,
                    y=entry[entry.columns[1]],
                    name=legend[1],
                    marker=dict(color='#07e40e')
                    )

    trace2 = go.Bar(x=entry.index,
                    y=entry[entry.columns[2]],
                    name=legend[2],
                    marker=dict(color='#FF0000')
                    )

    trace3 = go.Bar(x=entry.index,
                    y=entry[entry.columns[3]],
                    name=legend[3],
                    marker=dict(color='#ffff00')
                    )

    layout = go.Layout(title=title,
                       xaxis=go.layout.XAxis(
                           title='States',
                           showticklabels=False
                       ),
                       yaxis=go.layout.YAxis(
                           title=entry.columns[0]
                       ),
                       showlegend=True,
                       hovermode='x',
                       barmode='stack'
                       )
    fig = go.Figure(data=[trace, trace1, trace2, trace3], layout=layout)
    return plot(fig,
                output_type='div')

