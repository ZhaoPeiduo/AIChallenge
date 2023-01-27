import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
import datetime as dt
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

####################
# DATA IMPORT      #
####################
df = pd.read_csv('randomdata.csv')
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by='date', ascending=False)

####################
# Graph functions  #
####################

def score_by_day():
    daily_avg_score = pd.DataFrame(df.groupby(['date'])['score'].mean()).reset_index()
    fig = px.area(daily_avg_score, x='date', y='score', template = 'plotly_white')
    fig.update_layout(xaxis_title='Date', yaxis_title='Score')
    fig.update_layout(paper_bgcolor='rgb(250,250,250)')
    fig.update_traces(line=dict(color='#8B5E3C'))
    fig.update_layout(
        font=dict(
            family="Merriweather", # specify font family
            size=18,              # specify font size
            color="#7f7f7f"       # specify font color
        )
    )
    return fig

def piechart():
    df_byscore = pd.DataFrame(df.groupby("score").size()).reset_index()
    df_byscore.columns = ['score', 'count']
    pie_chart = px.pie(df_byscore, values = 'count', names = "score", hole = .3, 
                   color_discrete_sequence=['#8B6B62','#9E836F','#8F7C6B'],
                  labels = {"0":'neutral', 
                            "1":'positive', 
                            "-1":'negative'}, template="plotly_white")
    pie_chart.update_layout(paper_bgcolor='rgb(250,250,250)')
    pie_chart.update_layout(
        font=dict(
            family="Merriweather", # specify font family
            size=18,              # specify font size
            color="#7f7f7f"       # specify font color
        ),
        legend= dict(orientation = "h", x = 0.1, y = 0)
    )

    return pie_chart





SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    #"width": "20rem",
    "padding": "2rem",
    "background-color": "#f8f9fa",
}


MAIN_STYLE = {
    "padding": "2rem",
    }

#####################
# Side bar          #
#####################
sidebar = html.Div(
    [
        html.Div(children=[
            html.H5('Search Keyword'),
            html.Br(),
            dcc.Input(id='search-bar', placeholder='Search...'),
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H5("Please choose a date range"),

        html.Br(),
        html.Br(),

        html.Div([
            html.H6('Date'),
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
                html.Br(),
                html.H5("Average Score by Date", style = {'textAlign': 'center'}),
                dcc.Graph(id = "score by day", figure = score_by_day())
            ], style = {
                 "background-color": "#f8f8fa"
            })
        ], width = 7),
        dbc.Col([
            html.Div([
                html.Br(),
                html.H5("Proportion of Scores", style = {'textAlign': 'center'}),
                dcc.Graph(id = "piechart", figure = piechart())
            ], style = {
                 "background-color": "#f8f8fa"
            })
        ]),
    ]),
    html.Div(id='main-content', children = [
            ]),
], style = MAIN_STYLE)


####################
# APP LAYOUT       #
####################

app.layout = dbc.Row([
    dbc.Col(children=[
        sidebar
    ]),

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