import dash
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
from apps.app3 import get_df, download_df_from_sql

import base64
import datetime
import io

# ------------------------------------------------------------------------------
# Layout for table-page
def layout():

    #this is done in order to ensure that the dataframe exists in the application
    download_df_from_sql()
    try:
        df, len_df = get_df()
    except:
        return False, False

    #Graphic object
    return html.Div([ 
        html.Div(className='Row',children=[
                html.Div(className='col-lg-12 page-header',children=[
                    html.H3(className='text-center',children='Trykk \"generer tabell\" for å generere tabell med valgte filtre. Tabellen vil automatisk genereres ved færre enn 10000 treff')])
            ]),


        
        html.Br(), # Horizontal blank
        html.Br(), # Horizontal blank
 
        dcc.Dropdown(id='dropdown_state', style={'width': '150px'}, multi=False, placeholder = "Velg en stat"),
        dcc.Dropdown(id='dropdown_city',  style={'width': '150px'}, multi=False, placeholder = "Velg en by"),
        dcc.Dropdown(id='dropdown_street', style={'width': '150px'}, multi=False, placeholder = "Velg en gate"),

        html.P("Juster nedre og øvre grense på alder:"),
        html.Div(style = {'width': '60%', 'display': 'inline_block', 'align-items': 'center', 'justify-content': 'center'}, children=dcc.RangeSlider(id='slider_age',
                                              updatemode='drag',
                                              min=df["age"].min(),
                                              max=df["age"].max(),
                                              value=[df["age"].min(), df["age"].max()]
        )),
        html.Div(id='rng_slider_vals'),

        html.Br(), # Horizontal blank
        html.Br(), # Horizontal blank

        dcc.Input(id='search_input', placeholder="Søk ..."),

        html.Button(id="create-datatable-button", children="Generer tabell"),

        html.Hr(), # Horizontal line
        
        html.Hr(), # Horizontal line
        
        html.Div(id='output-datatable')
])

# ------------------------------------------------------------------------------
# Returns a dataframe based on provided filter values (state, city, street, age and free-text)
def filter(state=None, city=None, street=None, age=None, search_input=None):
    df, len_df = get_df()
    dff = df.copy()
    if state != None:
        dff = dff[dff["state"] == state]
    if city != None:
        dff = dff[dff["city"] == city]
    if street != None:
        dff = dff[dff["street"] == street]
    if age != None:
        dff = dff[(dff['age'] >= age[0]) & (dff['age'] <= age[-1])]
    if search_input != None:
        search_inputs = search_input.split()

        for s in search_inputs:
            strcols = ["name/first", "name/last", "street", "city", "state"]
            mask = np.column_stack([dff[col].str.contains(s, na=False) for col in strcols])
            dff = dff.loc[mask.any(axis=1)]

    return dff

# ------------------------------------------------------------------------------
# Load data table when user is interacting with button or sliders
@app.callback(Output('output-datatable', 'children'),
                Input('create-datatable-button', 'n_clicks'),
                Input('dropdown_state', 'value'),
                Input('dropdown_city', 'value'),
                Input('dropdown_street', 'value'),
                Input('slider_age', 'value'),
                State('search_input', 'value'))
def load_data_table(click, state, city, street, age, search_input):

    df, len_df = get_df()
    ctx = dash.callback_context

    # Checks if button is pressed (in contrast to slider manipulation)
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    #filter data based on dropdown menu
    dff = filter(state, city, street, age, search_input)

    #temp result value, in case no table is produced
    result = html.Div( html.P("Antall treff: " + str(len(dff.index))))

    #create table if button is pressed, or if table length is less than 10000
    if (button_id == "create-datatable-button") or len(dff.index) < 10000:
        result = html.Div([
    html.P("Antall treff: " + str(len(dff.index))),
    dash_table.DataTable(
        data=dff.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        columns=[{'name': i, 'id': i} for i in dff.columns],
        page_size=15
        ),])

    return result
        
# ------------------------------------------------------------------------------
# Create and update age-slider
@app.callback(Output('rng_slider_vals', 'children'),
              [Input('slider_age', 'value')])
def show_rng_slider_max_min(numbers):
    if numbers is None:
        raise PreventUpdate
    return 'Fra ' + ' Til: '.join([str(numbers[0]), str(numbers[-1])]) + ' år'

# ------------------------------------------------------------------------------
# Generate dynamic dropdown values for filtering on state, city, street and age
@app.callback(Output('dropdown_state', 'options'),
              Output('dropdown_city', 'options'),
                Output('dropdown_street', 'options'),
                Input('dropdown_state', 'value'),
              Input('dropdown_city', 'value'),
                Input('dropdown_street', 'value'),
                Input('slider_age', 'value'))
def update_dropdown(state, city, street, age):
        state_options= GenerateDropDownOptions("state")
        city_options = GenerateDropDownOptions("city", state=state)
        street_options = GenerateDropDownOptions("street", city=city)
        return [state_options, city_options, street_options]

# ------------------------------------------------------------------------------
# Returns drop-down options for callback function
def GenerateDropDownOptions(options_variable, state = None, city = None, street = None):
    df, len_df = get_df()
    dff = df.copy()
    if state != None:
        dff = dff[dff["state"] == state]
    if city != None:
        dff = dff[dff["city"] == city]
    return [{'label':x, 'value':x} for x in sorted(list(dict.fromkeys(dff[options_variable].tolist())))]


