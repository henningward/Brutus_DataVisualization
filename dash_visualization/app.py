import dash
import os
import dash_html_components as html

# Dash variable for application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server=app.server

