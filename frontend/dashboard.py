import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datetime

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

        html.Div([
            html.Label('Start Date'),
            dcc.DatePickerSingle(
                id='start-date',
                date=datetime.datetime.now()
            ),
        ]),

        html.Br(),
        html.Br(),
        html.Br(),

        html.Div([
            html.Label('End Date'),
            dcc.DatePickerSingle(
                id='end-date',
                date=datetime.datetime.now()
            )
        ])
    ],
    style = SIDEBAR_STYLE
)
#####################
# Main contents     #
#####################

contents = html.Div([
    html.H4("Place for graphs"),
    html.Div(id='main-content', children = [
            ]),
], style = MAIN_STYLE)

app.layout = dbc.Row([
    dbc.Col(className='sidebar', children=[
        sidebar
    ], width = 3),

    dbc.Col(children=[
            contents
        ], width = 9)
])

@app.callback(
    Output(component_id='main-content', component_property='children'),
    [Input(component_id='search-bar', component_property='value'),
     Input(component_id='start-date', component_property='date'),
     Input(component_id='end-date', component_property='date')]
)
def update_main_content(search_bar, start_date, end_date):
    return html.Div([
        html.H4('Search Results for {}'.format(search_bar)),
        html.P('Start Date: {}'.format(start_date)),
        html.P('End Date: {}'.format(end_date))
    ])

if __name__ == '__main__':
    app.run_server(debug=True)