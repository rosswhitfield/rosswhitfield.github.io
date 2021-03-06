#!/usr/bin/env python3
import json
from plotly.offline import plot
import plotly.graph_objs as go

with open('races.json') as f:
    data = json.load(f)

traces = []

for race_type in data['distances']:
    date = []
    pace = []
    text = []
    hovertext = []
    for race in data['races']:
        if race['type'] != race_type:
            continue
        date.append(race['date'])
        time = [int(x) for x in race['chip_time'].split(':')]
        time = (time[0]*60 + time[1])*60 + time[2]
        p = time/data['distances'][race['type']]
        pace.append(p/60)
        p2 = round(p*1.609)
        p = round(p)
        text.append('<a href="{url}">{name}</a> (<a href="{strava}">strava</a>)'.format(**race))
        hovertext.append("{name}<br>date: {date}<br>"
                         "time: {chip_time}<br>"
                         "pace: {0}m{1:02d}s/km ({2}m{3:02d}s/mi)<br>"
                         "position: {position}/{participants}".format(int(p/60), p % 60,
                                                                      int(p2/60), p2 % 60,
                                                                      **race))
    traces.append(go.Scatter(
        x=date,
        y=pace,
        mode='lines+markers+text',
        text=text,
        hovertext=hovertext,
        hoverinfo="text",
        name=race_type,
        marker=dict(size=20),
        textposition='middle right'
    ))

traces.append(go.Scatter(
    x=[],
    y=[],
    name='empty data to make yaxis2 appear',
    yaxis='y2'
))

layout = go.Layout(title='Races',
                   hovermode='closest',
                   xaxis=dict(
                       title='Date',
                       range=['2014-01-01', '2019-12-31'],
                       showgrid=False
                   ),
                   yaxis=dict(
                       title='Pace (min:sec/km)',
                       range=[5, 3.5],
                       gridwidth=5,
                       tickmode="array",
                       tickvals=[3.5, 3.75, 4, 4.25, 4.5, 4.75, 5],
                       ticktext=['3m30s', '3m45s', '4m00s', '4m15s', '4m30s', '4m45s', '5m00s'],
                       gridcolor='#dee'
                   ),
                   yaxis2=dict(
                       title='Pace (min:sec/mi)',
                       range=[8.045, 5.6315],
                       gridwidth=5,
                       tickmode="array",
                       tickvals=[6, 6.5, 7, 7.5, 8],
                       ticktext=['6m00s', '6m30s', '7m00s', '7m30s', '8m00s'],
                       side='right',
                       overlaying='y',
                       gridcolor='#ede'
                   ),
                   shapes=[
                       {
                           'type': 'rect',
                           'xref': 'x',
                           'yref': 'paper',
                           'x0': '2014-01-01',
                           'y0': 0,
                           'x1': '2014-12-31',
                           'y1': 1,
                           'fillcolor': '#d3d3d3',
                           'opacity': 0.2,
                           'line': {
                               'width': 0,
                           }
                       },
                       {
                           'type': 'rect',
                           'xref': 'x',
                           'yref': 'paper',
                           'x0': '2016-01-01',
                           'y0': 0,
                           'x1': '2016-12-31',
                           'y1': 1,
                           'fillcolor': '#d3d3d3',
                           'opacity': 0.2,
                           'line': {
                               'width': 0,
                           }
                       },
                       {
                           'type': 'rect',
                           'xref': 'x',
                           'yref': 'paper',
                           'x0': '2018-01-01',
                           'y0': 0,
                           'x1': '2018-12-31',
                           'y1': 1,
                           'fillcolor': '#d3d3d3',
                           'opacity': 0.2,
                           'line': {
                               'width': 0,
                           }
                       }
                   ],
                   legend=dict(
                       orientation="h")
                   )

fig = go.Figure(data=traces, layout=layout)

plot(fig,
     show_link=False,
     filename='races.html',
     auto_open=False)
