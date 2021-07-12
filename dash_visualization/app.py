import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

import pandas as pd

from dash.exceptions import PreventUpdate


global df
global df_filtered

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.layout = html.Div([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
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
    html.Div(id='output-div'),
    html.Div(id='output-datatable'),
    html.Div(id='output-datatable2'),
])

def filter(val):
    """
    For user selections, return the relevant in-memory data frame.
    """
    return df.loc[df.number.astype(str).str.contains(val)]


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

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # Create bar chart to display data
        # html.P("Insert X axis data"),
        dcc.Dropdown(id='xaxis-data',
                      options=[{'label':x, 'value':x} for x in df.columns]),
        html.P("Insert Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        # html.Button(id="submit-button", children="Create Graph"),
        
        # filter på stat, by, gate, alder
        html.P("Velg stat:"),
        #dcc.Dropdown(id='yaxis-data',
        #options=[{'label':x, 'value':x} for x in df["state"].tolist()]),
        dcc.Dropdown(id='dropdown_state', multi=False, placeholder = "Velg en stat"),
        dcc.Dropdown(id='dropdown_city', multi=False, placeholder = "Velg en by"),
        dcc.Dropdown(id='dropdown_street', multi=False, placeholder = "Velg en gate"),
        html.Div(children=dcc.RangeSlider(id='slider_age',
                                              updatemode='drag')),
        html.Div(id='rng_slider_vals'),
        html.Button(id="create-datatable-button", children="Generer tabell"),
        
        #dcc.Graph(id='bar-chart', figure={}),

        #dcc.Graph(id='map-plot', figure={}),
        

        html.Hr(), # Horizontal line


        # TABLE OF ALL DATA
        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     page_size=15
        # ),
        
        # Store data in browser
        #dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# ------------------------------------------------------------------------------
# Load file and parse data
@app.callback(Output('output-datatable', 'children'),
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
# Load data table when user is interacting with button
@app.callback(Output('output-datatable2', 'children'),
              Input('create-datatable-button', 'n_clicks'))

def load_data_table(clicks):
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     page_size=15
        # ),

        
# ------------------------------------------------------------------------------
# Create and update age-slider
@app.callback(Output('rng_slider_vals', 'children'),
              [Input('slider_age', 'value')])
def show_rng_slider_max_min(numbers):
    if numbers is None:
        raise PreventUpdate
    return 'from:' + ' to: '.join([str(numbers[0]), str(numbers[-1])])


# ------------------------------------------------------------------------------
# Generate dynamic dropdown values for filtering on state, city and street
def GenerateDropDownOptions(options_variable, state = None, city = None, street = None):
    dff = df.copy()
    if state != None:
        dff = dff[dff["state"] == state]
    if city != None:
        dff = dff[dff["city"] == city]
    return [{'label':x, 'value':x} for x in sorted(list(dict.fromkeys(dff[options_variable].tolist())))]



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
# Create bar chart based on user inputs
@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              #State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))
def make_bar_chart(n, x_data, y_data):
    if n is None:
        return dash.no_update
    else:
        dff = df.copy()
        
        #dff = dff[dff["Year"] == option_slctd]
        #bar_fig = px.bar(df, x=x_data, y=y_data)
        # print(data)
        
        return 0
#        return dcc.Graph(figure=bar_fig)






# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# @app.callback(
#     [Output(component_id='map-plot', component_property='figure')],
#     [Input('upload-data', 'contents')]
# #    State('stored-data','data'),]
# )
# def update_graph(option_slctd):


#     dff = df.copy()
#     #dff = dff[dff["Year"] == option_slctd]
#     #dff = dff[dff["Affected by"] == "Varroa_mites"]




#     # Plotly Express
#     fig = px.choropleth(
#         data_frame=dff,
#         locationmode='USA-states',
#         locations='state',
#         scope="usa",
#        # color='Pct of Colonies Impacted',
#        # hover_data=['State', 'Pct of Colonies Impacted'],
#         color_continuous_scale=px.colors.sequential.YlOrRd,
#         labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
#         template='plotly_dark'
#     )

#     Plotly Graph Objects (GO)
#     fig = go.Figure(
#         data=[go.Choropleth(
#             locationmode='USA-states',
#             locations=dff['state_code'],
#             z=dff["Pct of Colonies Impacted"].astype(float),
#             colorscale='Reds',
#         )]
#     )
    
#     fig.update_layout(
#         title_text="Bees Affected by Mites in the USA",
#         title_xanchor="center",
#         title_font=dict(size=24),
#         title_x=0.5,
#         geo=dict(scope='usa'),
#     )

#     return fig


# @app.callback(Output('output-div', 'children'),
#               Input('submit-button','n_clicks'),
#               State('stored-data','data'),
#               State('xaxis-data','value'),
#               State('yaxis-data', 'value'))
# def make_graphs(n, data, x_data, y_data):
#     if n is None:
#         return dash.no_update
#     else:
#         bar_fig = px.bar(data, x=x_data, y=y_data)
#         # print(data)
#         return dcc.Graph(figure=bar_fig)



if __name__ == '__main__':
    app.run_server(debug=True)