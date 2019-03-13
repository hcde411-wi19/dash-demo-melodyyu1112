# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import csv
from dash.dependencies import Input, Output, State

# initialize Dash app and initialize the static folder
app = dash.Dash(__name__, static_folder='static')


# print(pd)
class DataHandler(object):
    def __init__(self):
        sum_suicide, country_years = self.read_data()
        self.sum_suicide = sum_suicide
        self.country_years = country_years
        self.country = None
        self.current_data = {}
        self.current_graph = {}

        self.update_country()

    def read_data(self, filename='static/master_2.csv'):
        data = []
        with open('static/master_2.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)


        sum_suicide = {}
        country_years = []
        for row in data:
            country_year = row['country-year']
            country_years.append(country_year)
            if country_year not in sum_suicide:
                sum_suicide[country_year] = {
                    'male': 0,
                    'female': 0
                }

            sex = row['sex']
            sum_suicide[country_year][sex] += float(row['suicides_no'])

        return sum_suicide, country_years

    def extract_data(self, country=None, country_years=[]):
        male_data = [self.sum_suicide[country_year]['male'] for country_year in country_years]
        female_data = [self.sum_suicide[country_year]['female'] for country_year in country_years]
        return male_data, female_data

    def update_country(self, country=None):
        self.country = country
        if country is None:
            country_years = self.country_years
        else:
            country_years = [c for c in self.country_years if country in c]

        male_data, female_data = self.extract_data(country, country_years)

        self.current_data = {
            'x': country_years,
            'male_data': male_data,
            'female_data': female_data
        }



# new an object for keeping data
data_handler = DataHandler()


app.layout = html.Div(children=[
    # H1 title on the page
    html.H1(children='Suicidal Rate in Country/Year'),

    # a div to put a short description
    html.Label(children='Enter a country name:'),

    dcc.Input(id='symbol', value='', type='text'),
    html.Button(id='submit', type='submit', children='submit'),

    # append the visualization to the page
    dcc.Graph(
        id='linechart'
    ),
    dcc.Graph(
        id='linechart2'
    )
])


@app.callback(
    Output(component_id='linechart', component_property='figure'),
    [Input(component_id='symbol', component_property='n_submit'),
     Input(component_id='symbol', component_property='n_blur'),
     Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='symbol', component_property='value')]
)
def get_data(n_submit, n_blur, n_clicks, country):
    country = country.strip()
    if country == '':
        country = None

    data_handler.update_country(country)
    data_handler.current_graph = {
        # configure the data
        'data': [
            # This is how we define a scatter plot. Note that it also uses "go.Scatter",
            # but with the mode to be only "markers"
            go.Bar(
                x=data_handler.current_data["x"],
                y=data_handler.current_data["male_data"],
                text=data_handler.current_data["x"],  # This line sets the vehicle name as the points' labels.
                marker={
                    'color': 'rgb(49,130,189)'
                },
                opacity=0.5,
                name='Male'
            )
        ],
        'layout': {
            'title': 'Suicidal Rate in Country/Year',
            # It is always a good practice to have axis labels.
            # This is especially important in this case as the numbers are not trivial
            'barmode': 'stack',
            'xaxis': {'title': 'country-year'},
            'yaxis': {'title': 'suicides/ 100k pop', },
        }
    }

    return data_handler.current_graph


@app.callback(
    Output(component_id='linechart2', component_property='figure'),
    [Input(component_id='symbol', component_property='n_submit'),
     Input(component_id='symbol', component_property='n_blur'),
     Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='symbol', component_property='value')]
)
def get_data2(n_submit, n_blur, n_clicks, country):
    country = country.strip()
    if country == '':
        country = None

    data_handler.update_country(country)
    data_handler.current_graph = {
        # configure the data
        'data': [
            # This is how we define a scatter plot. Note that it also uses "go.Scatter",
            # but with the mode to be only "markers"
            go.Bar(
                x=data_handler.current_data["x"],
                y=data_handler.current_data["female_data"],
                text=data_handler.current_data["x"],  # This line sets the vehicle name as the points' labels.
                marker={
                    'color': 'rgb(128, 0, 0)'
                },
                opacity=0.5,
                name='Female'
            )
        ],
        'layout': {
            'title': 'Suicidal Rate in Country/Year',
            # It is always a good practice to have axis labels.
            # This is especially important in this case as the numbers are not trivial
            'barmode': 'stack',
            'xaxis': {'title': 'country-year'},
            'yaxis': {'title': 'suicides/ 100k pop', },
        }
    }

    return data_handler.current_graph


# start the app
if __name__ == '__main__':
    app.run_server()