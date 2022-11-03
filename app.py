import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output


def change_color(color):
    if color == "red":
        return "blue"
    return "red"


# https://dash.plotly.com/interactive-graphing
# https://community.plotly.com/t/convert-dash-to-executable-file-exe/14222/2
# https://stackoverflow.com/questions/63375135/python-dash-update-dataframe-every-60-minutes
# https://dash.plotly.com/deployment

hack_data = np.linspace(-10, 10, 1000)
hack_y = np.zeros(1000)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

styles = {'pre': {'border': 'thin lightgrey solid', 'overflowX': 'scroll'}}

fig = go.Figure()

# Create scatter trace of text labels
fig.add_trace(go.Scatter(x=hack_data, y=hack_y, mode='lines',
                         marker=dict(color='black', size=3),
                         opacity=1.0, showlegend=False))
fig.update_yaxes(range=[-0.25, 0.25],
                 fixedrange=True,
                 title="")
fig.update_xaxes(range=[-6, 6])
fig.add_shape(type='circle',
              editable=False,
              x0=1.00,
              x1=1.18,
              fillcolor="red",
              y0=-0.02,
              y1=0.02)
fig.add_shape(type='circle',
              editable=True,
              x0=0.0,
              x1=0.18,
              fillcolor="blue",
              y0=-0.02,
              y1=0.02)
print(fig.layout.shapes)

app.layout = html.Div(className='row', children=[
    dcc.Graph(
        id='basic-interactions',
        className='six columns',
        figure=fig
    ),
    html.Div(
        className='six columns',
        children=[
            html.Div(
                [
                    dcc.Markdown(
                        d("""
                **Zoom and Relayout Data**

            """)),
                    html.Pre(id='relayout-data', style=styles['pre']),
                ]
            )
        ]
    ),
    html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),
    html.Div(dcc.Checklist(["drag"], id="drag-points"))
])


@app.callback(
    [Output('click-data', 'children'),
     Output('basic-interactions', 'figure')],
    Input('basic-interactions', 'clickData'),
    Input('basic-interactions', 'figure'))
def display_click_data(clickData, figure):
    if clickData is not None:
        clicked = clickData["points"][0]["x"]
        for point in figure["layout"]["shapes"]:
            if not point["editable"]:
                if point["x0"] <= clicked and point["x1"] >= clicked:
                    point["fillcolor"] = change_color(point["fillcolor"])
    return json.dumps(clickData, indent=2), figure


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
