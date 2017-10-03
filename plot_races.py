#!/usr/bin/env python
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
        time = time[0]*60 + time[1] + time[2]/60
        p = time/data['distances'][race['type']]
        pace.append(p)
        text.append("{}".format(race['name']))
        p2 = p*1.609
        hovertext.append("{}<br>pace: {}m{}s/km ({}m{}s/mi)<br>position: {}/{}".format(race['name'],
                                                                                       int(p), int((p % 1)*60),
                                                                                       int(p2), int((p2 % 1)*60),
                                                                                       race['position'], race['participants']))
    traces.append(go.Scatter(
        x=date,
        y=pace,
        mode='lines+markers+text',
        text=text,
        hovertext=hovertext,
        hoverinfo="text",
        name=race_type
    ))

layout = go.Layout(title='Races',
                   hovermode='closest',
                   xaxis=dict(
                       title='Date',
                       range=['2014-01-01', '2018-01-01']
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
                   )
                   )

fig = go.Figure(data=traces, layout=layout)

plot(fig,
     show_link=False,
     filename='races.html',
     auto_open=False)
