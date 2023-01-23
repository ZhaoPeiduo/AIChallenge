from dash import Dash, html, Output, Input, dcc, State, dash_table
import runner
import pandas as pd
import plotly.express as px


class SampleApp:

    def __init__(self, word):
        self._word = word
        self._runner = None

    def load_data(self, model_result):
        data_dict = {"count": [0, 0, 0]}
        for res_dict in model_result:
            labels = res_dict["labels"]
            for label in labels:
                data_dict["count"][label + 1] += 1
        return data_dict

    # def load_statistics(self):
    #     df = pd.read_csv("./outputs/data.csv")
    #     total_likes = df["Likes"].fillna(0).sum()
    #     total_comments = df["Comments"].fillna(0).sum()
    #     total_retweets = df["Retweets"].fillna(0).sum()
    #     return total_likes, total_comments, total_retweets
    #
    # total_likes, total_comments, total_retweets = self.load_statistics()
    # Output('total comments', 'total comments'),
    # Output('total likes', 'total likes'),
    # Output('total retweets', 'total retweets')]
    # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

    def generate_chart(self, num_of_days, word, limit=40, driver_type="chrome"):
        self._runner = runner.Runner(num_of_days, word, limit, driver_type)
        model_result = self._runner()
        df = pd.DataFrame.from_dict(self.load_data(model_result))
        fig = px.pie(df, values='count', names=[-1, 0, 1], title='sentiment distribution')
        return fig

    def run_app(self):
        app = Dash(__name__)

        @app.callback(Output('sentiment graph', 'figure'),
                      [Input('submit_button', 'n_clicks')],
                      [State('num_of_days', 'value'), State('word', 'value')],
                      )
        def call_generate(n_clicks, num_of_days, word, limit=40, driver_type="chrome"):
            if n_clicks is not None:
                return self.generate_chart(num_of_days, word, limit, driver_type)

        app.layout = html.Div([
                        html.H4('Sentiment Analysis'),
                        dcc.Graph(id="sentiment graph"),
                        html.P("Number of days:"),
                        dcc.Input(id="num_of_days",
                                  value=5,
                                  type="number",
                                  min=0,
                                  max=10,
                                  step=1),
                        html.P("Word:"),
                        dcc.Input(id="word",
                                  value="covid",
                                  type="text"),
                        html.Button('Submit', id='submit_button', n_clicks=1)
                    ])

        app.run_server()


if __name__ == '__main__':
    sample_app = SampleApp("covid")
    sample_app.run_app()
