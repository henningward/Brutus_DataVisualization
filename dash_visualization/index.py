from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app
from apps import app1, app2, app3, app4
import base64
import os
from flask import send_from_directory


server=app.server

# ------------------------------------------------------------------------------
# Main layout of application. Creates navigation bar, and activates callback for choosing page
app.layout=html.Div([      
        html.Link(
    rel='stylesheet',
    href='/static/custom.css'),
    dcc.Location(id='url', refresh=False),
    html.Nav(id='nav',
    className='navbar navbar-default',children=html.Div(className='container-fluid',children=[html.Div(
            className='navbar-header',children=html.Div(className="navbar-brand",children='Brutus A/S')
        ),
        html.Ul(className='nav navbar-nav',children=[
        html.Li(children=html.A(href="/apps/tabell",children="Tabell")),
        html.Li(children=html.A(href="/apps/Grafer",children="Graf")),
        html.Li(children=html.A(href="/apps/Kart",children="Kart")),
        html.Li(children=html.A(href="/apps/LastOpp",children="Last opp fil")),
        ]),
        ])
    )
    
    ,html.Div(id='page-content')
])


# ------------------------------------------------------------------------------
# Callback for page navigation. 
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/tabell':
        return app1.layout()
    elif pathname == '/apps/Kart':
        return app2.layout()
    elif pathname == '/apps/LastOpp':
        return app3.layout()    
    elif pathname == '/apps/Grafer':
        return app4.layout()    

    # Goes to "upload" page
    else:
        return app3.layout()


# ------------------------------------------------------------------------------
# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
