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
# Layout for graph-page
def layout():
    if not df_exists():
        download_df_from_sql()
    df, len_df = get_df()
    dropdownopt = GenerateDropDownOptions()

    return html.Div([
            html.Div(className='Row',children=[
                html.Div(className='col-lg-12 page-header',children=[
                    html.H3(className='text-center',children='Aldersfordeling')])
            ]),

        dcc.Dropdown(id="select_graph_dropdown",
                    options= dropdownopt,
                    multi=False,
                    style={'width': "40%"}
                    ),

        html.Div(id='graph_output', children=[]),
        html.Br(),

        dcc.Graph(id='graph_plot', figure={}),
        
        ])

# ------------------------------------------------------------------------------
# Generate dropdown-values based on states
def GenerateDropDownOptions():
    df, len_df = get_df()
    return [{'label':x, 'value':x} for x in sorted(list(dict.fromkeys(df["state"].tolist())))]

# ------------------------------------------------------------------------------
# Callback for creating graph
@app.callback(
    [Output(component_id='graph_output', component_property='children'),
     Output(component_id='graph_plot', component_property='figure')],
    [Input(component_id='select_graph_dropdown', component_property='value'),])
def update_graph(option_slctd):
    df, len_df = get_df()
    
    if option_slctd == None:
        container = "Alder på brukere fordelt på alle stater"
    else:
        container = "Alder på brukere i {}".format(option_slctd)  
        df = df[df["state"] == option_slctd]

    #create temp lists
    ages = list(pd.unique(df['age']))
    count = [0] * len(ages)
    avg_age = [0] * len(ages)

    #iterate through all ages
    for age in ages:
        index = ages.index(age)
        #counting total numbers of clients in each state
        count[index] = df[df.age == age].shape[0]

        #creating new dataframe to filter on the selected state
        dff = df[df["age"] == age]
        avg_age[index] = round(dff["age"].sum()/count[index], 2)
    
    #create dictionary based on results
    d = {'age': ages, 'count': count, 'average_age': avg_age}

    #create dataframe
    dff = pd.DataFrame(d)

    clr = "count"
    if option_slctd == "gjennomsnittsalder":
        clr = "average_age"

    fig = px.bar(dff, x="age", y="count",
             labels={'age':'Alder', 'count': "antall"}, height=400, title=container)

    return None, fig
