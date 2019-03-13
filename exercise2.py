# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import csv



# Exercise 2
# Create another visualization of your choice of data and chart type.
# You can use pandas to help loading data, or just hard-coded the data is fine.
# -*- coding: utf-8 -*-
# initialize Dash app and initialize the static folder
app = dash.Dash(__name__, static_folder='static')
data = []
with open('static/master_2.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

#print(data)
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

male_data = [sum_suicide[country_year]['male'] for country_year in country_years]
female_data = [sum_suicide[country_year]['female'] for country_year in country_years]


# set layout of the page
app.layout = html.Div(children=[

    # set the page heading
    html.H1(children='Suicide Country/Year'),

    # set the description underneath the heading
    html.Div(children='''
    Showing by a stack bargraph
'''),

    # append the visualization to the page
    dcc.Graph(
        id='example-graph',
        figure={
            # configure the data
            'data': [
                # This is how we define a scatter plot. Note that it also uses "go.Scatter",
                # but with the mode to be only "markers"
                go.Bar(
                    x=country_years,
                    y=male_data,
                    text=country_years,  # This line sets the vehicle name as the points' labels.
                    marker={
                        'color': 'rgb(49,130,189)'
                    },
                    opacity=0.5,
                    name='Male'
                )
            ],
            'layout': {
                'title': 'Car Dataset 2004',
                # It is always a good practice to have axis labels.
                # This is especially important in this case as the numbers are not trivial
                'barmode': 'stack',
                'xaxis': {'title': 'country-year'},
                'yaxis': {'title': 'suicides/ 100k pop', },
            }
        }
    ),
    dcc.Graph(
        id='example-graph2',
        figure={
            # configure the data
            'data': [
                # This is how we define a scatter plot. Note that it also uses "go.Scatter",
                # but with the mode to be only "markers"

                go.Bar(
                    x=country_years,
                    y=female_data,
                    text=country_years,  # This line sets the vehicle name as the points' labels.
                    marker={
                        'color': 'rgba(219, 64, 82, 0.7)'
                    },
                    opacity=0.5,
                    name='Female'
                )
            ],
            'layout': {
                'title': 'Car Dataset 2004',
                # It is always a good practice to have axis labels.
                # This is especially important in this case as the numbers are not trivial
                'barmode': 'stack',
                'xaxis': {'title': 'country-year'},
                'yaxis': {'title': 'suicides/ 100k pop'},
            }
        }
    )

]

)

if __name__ == '__main__':
    app.run_server(debug=True)