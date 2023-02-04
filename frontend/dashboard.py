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
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

####################
# DATA IMPORT      #
####################
df = pd.read_csv('randomdata.csv')
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by='date', ascending=False)

#inital plan, not based on score yet
text = df['text']
str = text.to_string()
text = df['text']
type(text)
usetext = ''.join(text)


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
    plt.axis("off");


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
    df_byscore = df_byscore.replace([-1,0,1],['negative','neutral','positive'])
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
    daily_df['date']= pd.DatetimeIndex(daily_df.date).strftime("%Y-%m-%d")
    num = daily_df[property_str].sum()
    return daily_df, num
'''
Creating the top 4 small graphs using the x, y and num returned from df_by_date function
'''
def subplots(property_str):
    # Create the text and graph
    df, num=df_by_date(property_str)

    text = go.Scatter(x=[0], y=[0], mode='text', text=[f"{num}"], textfont={'size': 30},
                      textposition="middle left")
    graph = go.Scatter(x=df['date'], y=df[property_str], mode='lines', fill='tozeroy', line_color='#BEB5B4')

    # Create the subplot
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(graph)
    # fig.add_trace(text,secondary_y=True)

    fig = go.Figure()
    fig.add_trace(graph)
    fig.add_annotation(x=3.5,y='50%',text=f"{num:,d}",showarrow=False)


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
            dcc.Input(id='search-bar', placeholder='Search...', style={'display':'inline'}),
            html.Span("  "),
            html.Button(
                id='search_button',
                children=[
                    html.Img(id="search_img",src=app.get_asset_url('search-48.png'), style={'display':'inline'}),
                ],
                style={
                    'display': 'inline-block',
                    'width': '50px',
                    'height': '50px',
                    'border': 'none',
                    'background-color': '#BEB5B4',
                    'border-radius': '25px',
                    'text-align': 'center',
                    'position': 'relative'}
            )
            ,
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
                end_date=date.today(),
                stay_open_on_select=True
            ),
        ]),
    ],
    style=SIDEBAR_STYLE
)


#####################
# Main contents     #
#####################

contents = html.Div([
    html.H4("Sentiment Analysis of Tweets"),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='likes',figure= subplots('likes'), 
                          config={'displayModeBar': False}),
                html.Img(id="likes_img",src=app.get_asset_url('favorite-24.png'), style={'display':'inline'}),
                html.P("  Total number of likes by date", style={'textAlign': 'center', 'font-size':'10px','display':'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='comments', figure=subplots('comments'),
                config={'displayModeBar': False}),
                html.Img(id="comments_img",src=app.get_asset_url('comments-24.png'), style={'display':'inline'}),
                html.P("  Total number of comments by date", style={'textAlign': 'center', 'font-size':'10px', 'display':'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id='retweets', figure=subplots('retweets'),
                config={'displayModeBar': False}),
                html.Img(id="retweets_img",src=app.get_asset_url('retweet-24.png'), style={'display':'inline'}),
                html.P("  Total number of retweets by date", style={'textAlign': 'center', 'font-size':'10px','display':'inline'})
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Br(),
                dcc.Graph(id="num_tweets", figure=subplots('num_tweets'),
                config={'displayModeBar': False}),
                html.Img(id="tweets_img",src=app.get_asset_url('twitter-30.png'), style={'display':'inline', 'height':'25px','width':'25px'}),
                html.P("  Total number of tweets by date", style={'textAlign': 'center', 'font-size':'10px','display':'inline'})
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

'''
@app.callback(
    [
        Input(component_id='calendar', component_property='start_date'),
        Input(component_id='calendar', component_property='end_date')
    ]
)
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
