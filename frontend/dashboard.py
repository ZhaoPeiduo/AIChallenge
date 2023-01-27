import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
import datetime as dt
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


MAIN_STYLE = {
    "padding": "2rem 1rem"
}

#####################
# Side bar          #
#####################
sidebar = html.Div(
    [
        html.Div(children=[
            html.H4('Search Keyword'),
            html.Br(),
            dcc.Input(id='search-bar', placeholder='Search...'),
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H4("Please choose a date range"),

        html.Br(),
        html.Br(),

        html.Div([
            html.H5('Date'),
            dcc.DatePickerRange(
                id = "calendar",
                min_date_allowed=date.today()-dt.timedelta(days = 14),
                #start_date_placeholder_text="Start Period",
                #end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                max_date_allowed=date.today(),
                initial_visible_month=date.today()-dt.timedelta(days = 7),
                start_date = date.today()-dt.timedelta(days = 7),
                end_date = date.today()
            ),
        ]),
    ],
    style = SIDEBAR_STYLE
)
#####################
# Main contents     #
#####################

contents = html.Div([
    html.H4("Place for graphs"),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5("graph - 1")
            ], style = {
                 "background-color": "#f8f8fa"
            })
        ], width = 8),
        dbc.Col([
            html.Div([
                html.H5("graph - 2")
            ], style = {
                 "background-color": "#f8f8fa"
            })
        ], width = 4),
    ]),
    html.Div(id='main-content', children = [
            ]),
], style = MAIN_STYLE)


####################
# APP LAYOUT       #
####################

app.layout = dbc.Row([
    dbc.Col(className='sidebar', children=[
        sidebar
    ], width = 4),

    dbc.Col(children=[
            contents
        ], width = 8)
])

'''
@app.callback(
    [Output(component_id='calendar', component_property='end_date'),
     Output(component_id='warning', component_property='children')],
    [Input(component_id='calendar', component_property='start_date'),
     Input(component_id='range-picker', component_property='value')]
)
def update_end_date(start_date, value):
    out_of_range = False
    if value == "3 Days":
        if start_date + dt.timedelta(days = 3) > date.today():
            output1 = date.today()
    
    elif value == "1 Week":
    
    elif value == "2 Weeks":
    
'''

if __name__ == '__main__':
    app.run_server(debug=True)