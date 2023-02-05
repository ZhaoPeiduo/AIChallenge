import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import date
import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime
from runner import Runner
import itertools
from collections import Counter

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


def initialize_file():
    output_dir = os.path.join(os.curdir, "outputs")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    csv_file = os.path.join(output_dir, "data.csv")
    with open(csv_file, 'w') as f:
        f.write("userScreenName,userName,date,text,comments,likes,retweets,tweetURL,score")

####################
# GLOBAL VAR       #
####################
cur = {'start': datetime(2023, 1, 20), 'end': datetime(2023, 2, 4), 'keyword': "chatgpt"}
change = {'start': datetime(2023, 1, 20), 'end': datetime(2023, 2, 4), 'keyword': "chatgpt"}


####################
# DATA IMPORT      #
####################

def update_df():
    new_df = pd.read_csv('outputs/data.csv')
    new_df["date"] = pd.to_datetime(new_df["date"]).dt.date
    new_df = new_df.sort_values(by='date', ascending=False)
    return new_df


def get_data():
    global df, comments, likes, retweets
    comments = df.sort_values(by="comments", ascending=False)
    likes = df.sort_values(by="likes", ascending=False)
    retweets = df.sort_values(by="retweets", ascending=False)

    if df.size >= 3:
        comments = comments.head(3)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()
        likes = likes.head(3)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()
        retweets = retweets.head(3)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()
    else:
        comments = comments.head(df.size)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()
        likes = likes.head(df.size)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()
        retweets = retweets.head(df.size)[["date", "comments", "retweets", "likes", "text", "tweetURL"]].reset_index()


df = update_df()
comments = likes = retweets = pd.DataFrame()
get_data()

####################
# hashtags         #
####################

# Define a function to extract hashtags from each sentence
def extract_hashtags(sentence):
    hashtags = [word.split("#")[1].split()[0] for word in sentence.split() if "#" in word]
    return hashtags


def get_most_frequent_words():
    global df
    msg = 'No popular hashtag'
    if df.empty:
        return msg

    hash_col = df['text'].copy()
    # Apply the function to the 'sentences' column
    hash_col = hash_col.apply(extract_hashtags)
    hash_col = hash_col[hash_col.apply(lambda x: len(x) > 0)]
    flattened_words_list = list(itertools.chain(*hash_col.values))

    # Get the frequency of each word
    word_frequency = dict(Counter(flattened_words_list))

    # Get most frequent words
    most_frequent_words = [word for word, frequency in
                           sorted(word_frequency.items(), key=lambda item: item[1], reverse=True)[:3]]
    if len(most_frequent_words) > 0:
        msg = "Top hashtags :"

        for i in range(len(most_frequent_words)):
            if i > 3:
                break
            msg += most_frequent_words[i]
            msg += ","

    return msg


msg = get_most_frequent_words()

####################
# Code for recs   #
####################

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Trending Posts", className="card-title"),
                dcc.Dropdown(id="tweet-rec",
                             options=[
                                 {'label': 'By Comments', 'value': 'By Comments'},
                                 {'label': 'By Likes', 'value': 'By Likes'},
                                 {'label': 'By Retweets', 'value': 'By Retweets'}
                             ],
                             value='By Comments'
                             ),
                html.Br(),
                html.Div([
                    html.H4("# 1"),
                    html.Main(id="tweet-1", children=[comments["text"][0] if comments.size >= 1 else ""],
                              style={"font-size": "18px"}),
                    html.P(id="details_link1",
                           children=["Link: {}".format(comments["tweetURL"][0] if comments.size >= 1 else "")],
                           style={"font-size": "14px"}),
                    html.P(id="details-1",
                           children=["Post has received {} comments, {} likes and {} retweets. Published on {}"
                           .format(comments["comments"][0] if comments.size >= 1 else 0,
                                   comments["likes"][0] if comments.size >= 1 else 0,
                                   comments["retweets"][0] if comments.size >= 1 else 0,
                                   comments["date"][0] if comments.size >= 1 else 0)
                                     ], style={"font-size": "10px"})
                ], className="card-text", ),
                html.Hr(),
                html.Br(),
                html.Div([
                    html.H4("# 2"),
                    html.Main(id="tweet-2", children=[comments["text"][1] if comments.size >= 2 else ""],
                              style={"font-size": "18px"}),
                    html.P(id="details_link2",
                           children=["Link: {}".format(comments["tweetURL"][1] if comments.size >= 2 else "")],
                           style={"font-size": "14px"}),
                    html.P(id="details-2",
                           children=["Post has received {} comments, {} likes and {} retweets. Published on {}"
                           .format(comments["comments"][1] if comments.size >= 2 else 0,
                                   comments["likes"][1] if comments.size >= 2 else 0,
                                   comments["retweets"][1] if comments.size >= 2 else 0,
                                   comments["date"][1] if comments.size >= 2 else 0)
                                     ], style={"font-size": "10px"}),
                ], className="card-text", ),
                html.Hr(),
                html.Br(),
                html.Div([
                    html.H4("# 3"),
                    html.Main(id="tweet-3", children=[comments["text"][2] if comments.size >= 3 else ""],
                              style={"font-size": "18px"}),
                    html.P(id="details_link3",
                           children=["Link: {}".format(comments["tweetURL"][2] if comments.size >= 3 else "")],
                           style={"font-size": "14px"}),
                    html.P(id="details-3",
                           children=["Post has received {} comments, {} likes and {} retweets. Published on {}"
                           .format(comments["comments"][2] if comments.size >= 3 else 0,
                                   comments["likes"][2] if comments.size >= 3 else 0,
                                   comments["retweets"][2] if comments.size >= 3 else 0,
                                   comments["date"][2] if comments.size >= 3 else 0)
                                     ], style={"font-size": "10px"}),
                ], className="card-text", ),
            ]
        ),
    ],
    style={"width": "55rem", "background-color": "#f8f9fa", "font-family": "Merriweather"},
)


####################
# Word Cloud     #
####################
# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")


####################
# LAYOUT SETTINGS  #
####################
def apply_standard_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgb(250,250,250)',
        font=dict(
            family="Merriweather",  # specify font family
            size=18,  # specify font size
            color="#7f7f7f"  # specify font color
        )
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
    df_byscore = df_byscore.replace([-1, 0, 1], ['negative', 'neutral', 'positive'])
    df_byscore.columns = ['score', 'count']
    pie_chart = px.pie(df_byscore, values='count', names="score", hole=.3,
                       color_discrete_sequence=['#8B6B62', '#9E836F', '#8F7C6B'],
                       template="plotly_white")
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


'''
For easy sketching of the graph, input = "comments", "likes", "retweets" or "num_tweets",
returning x, y (series for plotting), and the tally sum
 '''


def df_by_date(property_str):
    if property_str == "num_tweets":
        daily_df = pd.DataFrame(df.groupby(['date']).size()).reset_index()
    else:
        daily_df = pd.DataFrame(df.groupby(['date'])[property_str].sum()).reset_index()
    daily_df.columns = ['date', property_str]
    daily_df['date'] = pd.DatetimeIndex(daily_df.date).strftime("%Y-%m-%d")
    num = daily_df[property_str].sum()
    return daily_df, num


'''
Creating the top 4 small graphs using the x, y and num returned from df_by_date function
'''


def subplots(property_str):
    # Create the text and graph
    df, num = df_by_date(property_str)

    # text = go.Scatter(x=[0], y=[0], mode='text', text=[f"{num}"], textfont={'size': 30},
    #                   textposition="middle center")
    graph = go.Scatter(x=df['date'], y=df[property_str], mode='lines', fill='tozeroy', line_color='#BEB5B4')

    # Create the subplot
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(graph)
    # fig.add_trace(text,secondary_y=True)

    fig = go.Figure()
    fig.add_trace(graph)
    fig.add_annotation(x='50%', y='50%', text=f"{num:,d}", showarrow=False)

    # Update the layout
    fig.update_layout(
        font=dict(size=20, color='grey'),
        showlegend=False,
        paper_bgcolor='#F0EFEF',
        plot_bgcolor='#F0EFEF',
        height=100,
        width=200,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    fig.update_xaxes(type="category")

    # Remove the x-axis and y-axis
    fig.update_xaxes(showticklabels=False, showgrid=False, visible=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, visible=False)

    # Change the hoverlabel
    # fig.update_traces(hoverlabel=dict{

    # })

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
            dcc.Input(id='search-bar', placeholder='chatgpt', style={'display': 'inline'}),
            html.Span("  "),
            html.Button(
                id='search_button',
                children=[
                    html.Img(id="search_img", src=app.get_asset_url('search-48.png'), style={'display': 'inline'}),
                ],
                style={
                    'display': 'inline-block',
                    'width': '50px',
                    'height': '50px',
                    'border': 'none',
                    'background-color': '#BEB5B4',
                    'border-radius': '25px',
                    'text-align': 'center',
                    'position': 'relative'},
                n_clicks=-1
            ),

        ]),
        html.Br(),
        dbc.Progress(
            value=50, id="animated-progress", animated=True, striped=True, color="success"
        ),
        html.Br(),
        html.H5("Please choose a date range"),

        html.Br(),
        html.Br(),

        html.Div([
            html.H6('Date'),
            dcc.DatePickerRange(
                id="calendar",
                # min_date_allowed=date.today() - dt.timedelta(days=14),
                # start_date_placeholder_text="Start Period",
                # end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                # max_date_allowed=date.today(),
                initial_visible_month=datetime(2023, 1, 1),
                # start_date=datetime(2023, 1, 20),
                # end_date=datetime(2023, 2, 4),
                stay_open_on_select=True
            ),
        ]),
        html.Div(id="placeholder", children=[""])
    ],
    style=SIDEBAR_STYLE
)

#####################
# Main contents     #
#####################

contents = html.Div([
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Search Failed")),
            dbc.ModalBody(
                "The model cannot analyse the sentiments of the tweets in the given keyword and time period, please try again")
        ],
        id="modal_no_result",
        size="lg",
        is_open=False,
    ),
    html.H4("Sentiment Analysis of Tweets"),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='likes', figure=subplots('likes'),
                          config={'displayModeBar': False}),
                html.Img(id="likes_img", src=app.get_asset_url('favorite-24.png'), style={'display': 'inline'}),
                html.P("  Total number of likes by date",
                       style={'textAlign': 'center', 'font-size': '10px', 'display': 'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='comments', figure=subplots('comments'),
                          config={'displayModeBar': False}),
                html.Img(id="comments_img", src=app.get_asset_url('comments-24.png'), style={'display': 'inline'}),
                html.P("  Total number of comments by date",
                       style={'textAlign': 'center', 'font-size': '10px', 'display': 'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='retweets', figure=subplots('retweets'),
                          config={'displayModeBar': False}),
                html.Img(id="retweets_img", src=app.get_asset_url('retweet-24.png'), style={'display': 'inline'}),
                html.P("  Total number of retweets by date",
                       style={'textAlign': 'center', 'font-size': '10px', 'display': 'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id="num_tweets", figure=subplots('num_tweets'),
                          config={'displayModeBar': False}),
                html.Img(id="tweets_img", src=app.get_asset_url('twitter-30.png'),
                         style={'display': 'inline', 'height': '25px', 'width': '25px'}),
                html.P("  Total number of tweets by date",
                       style={'textAlign': 'center', 'font-size': '10px', 'display': 'inline'})
            ])

        ])

    ]),
    html.Br(),
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
    html.Div(id='main-content', children=[
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        html.Div([
            html.Img(id="hashtag_img", src=app.get_asset_url('hashtag.png'),
                     style={'display': 'inline', 'width': '25px', 'height': '25px'}),
            html.H4(id="hashtag_msg", style={'style': 'inline', 'font-size': '25px'})
        ],
        )
    ]),
    html.Br(),
    html.Br(),
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
    global df
    df = update_df()

    if value == "By Comments":
        data = comments
    elif value == "By Likes":
        data = likes
    elif value == "By Retweets":
        data = retweets

    null_tweet = "No post yet..."
    null_message = "No details yet..."

    tweet1 = tweet2 = tweet3 = null_tweet
    details1 = details2 = details3 = null_message

    if df.size >= 1:
        tweet1 = data["text"][0]
        details1 = "Post has received {} comments, {} likes and {} retweets. Published on {}".format(
            data["comments"][0], data["likes"][0], data["retweets"][0], data["date"][0])

    if df.size >= 2:
        tweet2 = data["text"][1]
        details2 = "Post has received {} comments, {} likes and {} retweets. Published on {}".format(
            data["comments"][1], data["likes"][1], data["retweets"][1], data["date"][1])

    if df.size >= 3:
        tweet3 = data["text"][2]
        details3 = "Post has received {} comments, {} likes and {} retweets. Published on {}".format(
            data["comments"][2], data["likes"][2], data["retweets"][2], data["date"][2])

    return tweet1, details1, tweet2, details2, tweet3, details3

computing = False

@app.callback(
    [Output("search_button",'disabled'),
     Output("placeholder", 'children'),
     Output('likes', 'figure'),
     Output('comments', 'figure'),
     Output('retweets', 'figure'),
     Output('num_tweets', 'figure'),
     Output('score by day', 'figure'),
     Output('piechart', 'figure'),
     Output('tweet-rec', 'value'),
     Output('hashtag_msg', 'children'),
     Output('modal_no_result', 'is_open')],
    [Input('search_button', 'n_clicks')],
    [State('search-bar', 'value'),
     State('calendar', 'start_date'),
     State('calendar', 'end_date')],
)
def run_backend(n_clicks, value, start_date, end_date):
    global cur, change, df, msg, computing
    temp_likes = subplots('likes')
    temp_comments = subplots('comments')
    temp_retweets = subplots('retweets')
    temp_numtweets = subplots('num_tweets')
    temp_scorebyday = score_by_day()
    temp_pie = piechart()
    is_no_result = False
    temp_msg = msg
    if computing:
        return True, [""], temp_likes, temp_comments, temp_retweets, temp_numtweets, temp_scorebyday, temp_pie, "By Comments", \
           temp_msg, is_no_result
    print("ok until here", flush=True)
    if value is not None and start_date is not None and end_date is not None:
        print("Passed checks..", flush=True)
        change['start'] = datetime.strptime(start_date, "%Y-%m-%d")
        change['end'] = datetime.strptime(end_date, "%Y-%m-%d")
        change['keyword'] = value
        if cur != change:
            cur = change
            print("searching...", flush=True)
            computing = True
            runner = Runner(cur['start'], cur['end'], cur['keyword'], 40, "chrome")
            runner()  # Call the __call__ method
            df = update_df()
            if df.empty:
                is_no_result = True
            get_data()
            temp_likes = subplots('likes')
            temp_comments = subplots('comments')
            temp_retweets = subplots('retweets')
            temp_numtweets = subplots('num_tweets')
            temp_scorebyday = score_by_day()
            temp_pie = piechart()
            temp_msg = get_most_frequent_words()
            msg = temp_msg
    print(n_clicks, "return from call backend", flush=True)
    computing = False
    return False, [""], temp_likes, temp_comments, temp_retweets, temp_numtweets, temp_scorebyday, temp_pie, "By Comments", \
           temp_msg, is_no_result


if __name__ == '__main__':
    initialize_file()
    app.run_server(debug=True, threaded=False)
