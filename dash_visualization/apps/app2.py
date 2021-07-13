from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate

import plotly.express as px

import pandas as pd
import numpy as np

from app import app
from apps.app3 import get_df, download_df_from_sql, df_exists

import base64
import datetime
import io


# ------------------------------------------------------------------------------
# Layout for map-page
def layout():
    if not df_exists():
        download_df_from_sql()
    df, len_df = get_df()

    return html.Div([
            html.Div(className='Row',children=[
                html.Div(className='col-lg-12 page-header',children=[
                    html.H3(className='text-center',children='Kart')])
            ]),

        dcc.Dropdown(id="select_map_dropdown",
                    options=[
                        {"label": "Gjennomsnittsalder", "value": "gjennomsnittsalder"},
                        {"label": "Antall brukere", "value": "antall brukere"}],
                    multi=False,
                    value="antall brukere",
                    style={'width': "40%"}
                    ),

        html.Div(id='map_div_output', children=[]),
        html.Br(),

        dcc.Graph(id='map-plot', figure={}),
        ])

# ------------------------------------------------------------------------------
# Callback for creating map
@app.callback(
    [Output(component_id='map_div_output', component_property='children'),
     Output(component_id='map-plot', component_property='figure')],
    [Input(component_id='select_map_dropdown', component_property='value'),]
)
def update_map(option_slctd):
    df, len_df = get_df()
    container = "Kartet illustrerer {} fordelt på stater".format(option_slctd)

    #create  temporary lists
    states = list(pd.unique(df['state']))
    count = [0] * len(states)
    avg_age = [0] * len(states)

    #iterate through states to populate temp lists
    for state in states:
        index = states.index(state)
        #counting total numbers of clients in each state
        count[index] = df[df.state == state].shape[0]

        #creating new dataframe to filter on the selected state
        dff = df[df["state"] == state]
        avg_age[index] = round(dff["age"].sum()/count[index], 2)
    
    #create dictionary based on results
    d = {'state': states, 'count': count, 'average_age': avg_age}

    #create dataframe
    dff = pd.DataFrame(d)

    clr = "count"
    if option_slctd == "gjennomsnittsalder":
        clr = "average_age"

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state',
        scope='usa',
        color= clr,
        hover_data=['state', 'count', 'average_age'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Brukerdatafordeling / USA'},
        template='plotly_dark'
    )

    return container, fig

