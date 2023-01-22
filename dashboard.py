from dash import Dash, html, Output, Input, dcc, State
import runner
import pandas as pd
import plotly.express as px


class SampleApp:

    def __init__(self, word):
        self._word = word
        self._runner = None

    def load_data(self, model_result):
        data_dict = {-1: 0, 0: 0, 1: 0}
        for res_dict in model_result:
            labels = res_dict["labels"]
            for label in labels:
                data_dict[label] += 1
        return data_dict

    def generate_chart(self, num_of_days, word, limit=40, driver_type="chrome"):
        self._runner = runner.Runner(num_of_days, word, limit, driver_type)
        model_result = self._runner()
        df = pd.DataFrame.from_dict(self.load_data(model_result))
        fig = px.pie(df, values='value', names='label', title='sentiment distribution')
        return fig

    def run_app(self):
        app = Dash(__name__)

        @app.callback(Output('graph', 'figure'),
                      [Input('submit_button', 'n_clicks')],
                      [State('num_of_days', 'value'), State('word', 'value')],
                      )
        def call_generate(n_clicks, num_of_days, word, limit=40, driver_type="chrome"):
            if n_clicks is not None:
                return self.generate_chart(num_of_days, word, limit, driver_type)

        app.layout = html.Div([
            html.H4('Sentiment Analysis'),
            dcc.Graph(id="graph"),
            html.P("Number of days:"),
            dcc.Input(id="num_of_days",
                      value="Input number of days here...",
                      type="number",
                      min=0,
                      max=10,
                      step=1),
            html.P("Word:"),
            dcc.Input(id="word",
                      value="Input search keyword here...",
                      type="text"),
            html.Button('Submit', id='submit_button', n_clicks=1)
        ])

        app.run_server()


if __name__ == '__main__':
    sample_app = SampleApp("covid")
    sample_app.run_app()
