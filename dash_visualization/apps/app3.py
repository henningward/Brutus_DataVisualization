from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

#import mysql.connector
#from mysql.connector import Error
import sqlalchemy
from sqlalchemy import create_engine
import pyodbc

import pandas as pd
import numpy as np
from app import app

import base64
import datetime
import io


#global dataframe variable.. 
global df 
global online
# ------------------------------------------------------------------------------
# Returns dataframe
def get_df():
    return df, len(df.index)

# ------------------------------------------------------------------------------
# Downloads the "brutus" table from mySQL-server
def download_df_from_sql():
    global df
    global online
    success = False

    try:
        sqlEngine = create_engine("mysql+pymysql://ward:Password123@192.168.0.67:3306/ward")
        dbConnection = sqlEngine.connect()
        df = pd.read_sql_query('''SELECT * FROM brutus''', con=dbConnection)
        success = True
        online = True
    except ValueError as vx:

        print(vx)

    except Exception as ex:   
        # Table probably does not exist
        print(ex)

    else:

        print("Data retreived successfully, with length %s."%len(df.index))   
    
#    finally:

        dbConnection.close()
        print("MySQL connection is closed")
    return success

# ------------------------------------------------------------------------------
# Uploads the current dataframe to "brutus" table in mySQL-server
def upload_df_to_sql():
    success = False

    tableName = "brutus"
    try:
        sqlEngine = create_engine("mysql+pymysql://ward:Password123@192.168.0.67:3306/ward")
        dbConnection = sqlEngine.connect()
        frame = df.to_sql(tableName, dbConnection, if_exists='replace')
        success = True
    
    except ValueError as vx:

        print(vx)

    except Exception as ex:   

        print(ex)

    else:

        print("Table %s created successfully."%tableName)   

    #finally:

        dbConnection.close()
        print("MySQL connection is closed")

    return success

# ------------------------------------------------------------------------------
# Layout for data-upload page
def layout():
    
    return html.Div([ 
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Dra og slipp, eller ',
            html.A('velg fil')
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
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Button(id="download-from-database-button", children="Last ned forrige versjon"),
    html.Div(id='file-download-success'),

    html.Div(id='output-file'),
])

# ------------------------------------------------------------------------------
# Parse data from csv-file to pandas df
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            global df
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

    if upload_df_to_sql() == True:
        return html.Div([
            html.P("Filen ble lastet opp!"),
            html.P("Database oppdatert!"),
            html.H5("filnavn: " + filename),])
    else:
        return html.Div([
            html.P("Filen ble lastet opp lokalt!"),
            html.P("Database kunne ikke oppdateres!"),
            html.H5("filnavn: " + filename),])

# ------------------------------------------------------------------------------
# Load file and parse data
@app.callback(Output('output-file', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# ------------------------------------------------------------------------------
# Download data manually from database (button)
@app.callback(Output('file-download-success', 'children'),
                Input('download-from-database-button', 'n_clicks'))
def download_from_database(clicks):
    if download_df_from_sql():
        result =  html.Div(html.P("Data lastet ned!")) 
    else:
        result =  html.Div(html.P("Filen kunne ikke lastes ned fra serveren")) 

    return result
