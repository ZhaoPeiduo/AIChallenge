import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

####################
# DATA IMPORT      #
####################
df = pd.read_csv('randomdata.csv')
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by='date', ascending=False)

####################
# Code for recs   #
####################
comments = df.sort_values(by="comments", ascending=False).head(3)[["date", "comments", "retweets", "likes", "text"]].reset_index()
likes = df.sort_values(by="likes", ascending=False).head(3)[["date", "comments", "retweets", "likes", "text"]].reset_index()
retweets = df.sort_values(by="retweets", ascending=False).head(3)[["date", "comments", "retweets", "likes", "text"]].reset_index()


card = dbc.Card(
    [
            dbc.CardBody(
            [
                html.H4("Trending Posts", className="card-title"),
                dcc.Dropdown(id = "tweet-rec",
                    options = [
                        {'label': 'By Comments', 'value': 'By Comments'},
                        {'label': 'By Likes', 'value': 'By Likes'},
                        {'label': 'By Retweets', 'value': 'By Retweets'}
                    ],
                    value='By Comments'
                ),
                html.Br(),
                html.Div([
                    html.H4("# 1"),
                    html.Main(id = "tweet-1", children = [comments["text"][0]], style = {"font-size": "18px"}),
                    html.P(id = "details-1", children =["Post has received {} comments, {} likes and {} retweets. Published on {}".format(comments["comments"][0], comments["likes"][0], comments["retweets"][0], comments["date"][0])
                    ], style = {"font-size": "10px"}),
                ], className="card-text",),
                html.Hr(),
                html.Br(),
                html.Div([
                    html.H4("# 2"),
                    html.Main(id = "tweet-2", children = [comments["text"][1]], style = {"font-size": "18px"}),
                    html.P(id = "details-2", children =["Post has received {} comments, {} likes and {} retweets. Published on {}".format(comments["comments"][1], comments["likes"][1], comments["retweets"][1], comments["date"][1])
                    ], style = {"font-size": "10px"}),
                ], className="card-text",),
                html.Hr(),
                html.Br(),
                html.Div([
                    html.H4("# 3"),
                    html.Main(id = "tweet-3", children = [comments["text"][2]], style = {"font-size": "18px"}),
                    html.P(id = "details-3", children =["Post has received {} comments, {} likes and {} retweets. Published on {}".format(comments["comments"][2], comments["likes"][2], comments["retweets"][2], comments["date"][2])
                    ], style = {"font-size": "10px"}),
                ], className="card-text",),
            ]
        ),
    ],
    style={"width": "25rem", "background-color": "#f8f9fa", "font-family": "Merriweather"},
)


####################
# Graph functions  #
####################

def score_by_day():
    daily_avg_score = pd.DataFrame(df.groupby(['date'])['score'].mean()).reset_index()
    fig = px.area(daily_avg_score, x='date', y='score', template='plotly_white')
    fig.update_layout(xaxis_title='Date', yaxis_title='Score')
    # fig.update_layout(paper_bgcolor='rgb(250,250,250)')
    fig.update_traces(line=dict(color='#8B5E3C'))
    # fig.update_layout(
    #     paper_bgcolor='rgb(250,250,250)',
    #     font=dict(
    #         family="Merriweather",  # specify font family
    #         size=18,  # specify font size
    #         color="#7f7f7f"  # specify font color
    #     )
    # )
    apply_standard_layout(fig)

    return fig


def piechart():
    df_byscore = pd.DataFrame(df.groupby("score").size()).reset_index()
    df_byscore.columns = ['score', 'count']
    pie_chart = px.pie(df_byscore, values='count', names="score", hole=.3,
                       color_discrete_sequence=['#8B6B62', '#9E836F', '#8F7C6B'],
                       labels={"0": 'neutral',
                               "1": 'positive',
                               "-1": 'negative'}, template="plotly_white")
    pie_chart.update_layout(paper_bgcolor='rgb(250,250,250)')
    pie_chart.update_layout(
        font=dict(
            family="Merriweather",  # specify font family
            size=18,  # specify font size
            color="#7f7f7f"  # specify font color
        ),
        legend=dict(orientation="h", x=0.1, y=0)
    )

    return pie_chart


def apply_standard_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgb(250,250,250)',
        font=dict(
            family="Merriweather",  # specify font family
            size=18,  # specify font size
            color="#7f7f7f"  # specify font color
        )
    )


def df_by_date(property_str):
    daily_avg = pd.DataFrame(df.groupby(['date'])[property_str].sum()).reset_index()
    daily_avg.columns = ['date', property_str]
    x=daily_avg['date']
    y=daily_avg[property_str]
    num = y.sum()
    return x, y, num


def num_tweets_by_day():
    daily_tweet = pd.DataFrame(df.groupby(['date']).size()).reset_index()
    daily_tweet.columns = ['date', 'num']
    fig = px.line(daily_tweet, x='date', y='num', template='plotly_white')
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of tweets')
    apply_standard_layout(fig)
    return fig

def subplots(property_str):
    # Create the text and graph
    X, Y, num=df_by_date(property_str)

    text = go.Scatter(x=[0], y=[0], mode='text', text=[f"{num}"], textfont={'size': 10},
                      textposition="middle center")
    graph = go.Scatter(x=X, y=Y, mode='lines', fill='tozeroy', line_color='white')

    # Create the subplot
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(graph)
    fig.add_trace(text)

    # Update the layout
    fig.update_layout(
        font=dict(size=20, color='grey'),
        showlegend=False,
        paper_bgcolor='#F0EFEF',
        plot_bgcolor='#F0EFEF',
        height = 100,
        width = 200,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    fig.update_xaxes(type="category")

    # Remove the x-axis and y-axis
    fig.update_xaxes(showticklabels=False, showgrid=False, visible=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, visible=False)

    return fig


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    # "width": "20rem",
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
                id="calendar",
                min_date_allowed=date.today() - dt.timedelta(days=14),
                # start_date_placeholder_text="Start Period",
                # end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                max_date_allowed=date.today(),
                initial_visible_month=date.today() - dt.timedelta(days=7),
                start_date=date.today() - dt.timedelta(days=7),
                end_date=date.today()
            ),
        ]),
    ],
    style=SIDEBAR_STYLE
)
#####################
# Main contents     #
#####################

contents = html.Div([
    html.H4("Place for graphs"),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id='likes',figure= subplots('likes'))
            ])
        ]),
        dbc.Col([
            html.Div([
                dcc.Graph(id='comments', figure=subplots('comments'))
            ])
        ]),
        dbc.Col([
            html.Div([
                dcc.Graph(id='retweets', figure=subplots('retweets'))
            ])
        ]),
        dbc.Col([
            dcc.Graph(id="num_tweets", figure=num_tweets_by_day())
        ])

    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Br(),
                html.H5("Average Score by Date", style={'textAlign': 'center'}),
                dcc.Graph(id="score by day", figure=score_by_day())
            ], style={
                "background-color": "#f8f8fa"
            })
        ], width=7),
        dbc.Col([
            html.Div([
                html.Br(),
                html.H5("Proportion of Scores", style={'textAlign': 'center'}),
                dcc.Graph(id="piechart", figure=piechart())
            ], style={
                "background-color": "#f8f8fa"
            })
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            # recommended tweets
            card
        ])
    ])
], style=MAIN_STYLE)

####################
# APP LAYOUT       #
####################

app.layout = dbc.Row([
    dbc.Col(children=[
        sidebar
    ]),

    dbc.Col(children=[
        contents
    ], width=8)
])


@app.callback([
    Output('tweet-1', 'children'),
    Output('details-1', 'children'),
    Output('tweet-2', 'children'),
    Output('details-2', 'children'),
    Output('tweet-3', 'children'),
    Output('details-3', 'children'),
], [Input('tweet-rec', 'value')])

def update_recs(value):
    if value == "By Comments":
        data = comments
    elif value == "By Likes":
        data = likes
    elif value == "By Retweets":
        data = retweets
    tweet1 = data["text"][0]
    details1= "Post has received {} comments, {} likes and {} retweets. Published on {}".format(data["comments"][0], data["likes"][0], data["retweets"][0], data["date"][0])
    tweet2=data["text"][1]
    details2="Post has received {} comments, {} likes and {} retweets. Published on {}".format(data["comments"][1], data["likes"][1], data["retweets"][1], data["date"][1])
    tweet3=data["text"][2]
    details3="Post has received {} comments, {} likes and {} retweets. Published on {}".format(data["comments"][2], data["likes"][2], data["retweets"][2], data["date"][2])

    return tweet1, details1, tweet2, details2, tweet3, details3


if __name__ == '__main__':
    app.run_server(debug=True)
