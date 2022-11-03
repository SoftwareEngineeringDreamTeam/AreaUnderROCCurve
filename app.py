# import json
# from textwrap import dedent as d
import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output


def change_color(color):
    if color == "red":
        return "blue"
    return "red"


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


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

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=hack_data, y=hack_data**2, mode='lines'))

fig = go.Figure()

# Create scatter trace of text labels
fig.add_trace(go.Scatter(x=hack_data, y=hack_y, mode='lines',
                         marker=dict(color='black', size=3),
                         opacity=1.0, showlegend=False))
fig.update_yaxes(range=[-0.25, 0.25],
                 fixedrange=True,
                 title="",
                 showgrid=False)
fig.update_xaxes(range=[-6, 6])
fig.add_shape(type='circle',
              editable=False,
              x0=1.0,
              x1=1.4,
              fillcolor="red",
              y0=-0.02,
              y1=0.02)
fig.add_shape(type='circle',
              editable=True,
              x0=0.0,
              x1=0.4,
              fillcolor="blue",
              y0=-0.02,
              y1=0.02)
fig.update_layout(template="plotly_white")


app.layout = html.Div(className='row', children=[
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Don't allow multiple files to be uploaded
        multiple=False
    ),
    dcc.Graph(
        id='fig1',
        className='five columns',
        figure=fig1
    ),
    dcc.Graph(
        id='fig2',
        className='five columns',
        figure=fig1
    ),

    dcc.Graph(
        id='basic-interactions',
        className='six columns',
        figure=fig
    ),
    dcc.Slider(-6, 6, 1,
               value=0,
               id='thr_slider'),
    # html.Div(dcc.Markdown("""**Score 1**
    #                     """),
    #          className='three columns'),
    # html.Div(id='slider-output-container', className='three columns')
])


# @app.callback(
#     Output('slider-output-container', 'children'),
#     Input('thr_slider', 'value'))
# def update_output(value):
#     return 'You have selected {}.'.format(value)


@app.callback(
    Output('basic-interactions', 'figure'),
    Input('basic-interactions', 'clickData'),
    Input('basic-interactions', 'figure'))
def display_click_data(clickData, figure):
    if clickData is not None:
        clicked = clickData["points"][0]["x"]
        for point in figure["layout"]["shapes"]:
            if not point["editable"]:
                if point["x0"] <= clicked and point["x1"] >= clicked:
                    point["fillcolor"] = change_color(point["fillcolor"])
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
