from dash import dcc, html, Input, Output, Dash
import plotly.express as px
import pandas as pd

world_cup = pd.DataFrame({
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    "Winners": ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "England", "Brazil", "Germany", "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "Runners-up": ["Argentina", "Czech Republic", "Hungary", "Brazil", "Hungary", "Sweden", "Czech Republic", "Germany", "Italy", "Netherlands", "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"]
})

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('World Cup Winners', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='world_cup_dropdown',
        options=[
            {'label': 'Winners', 'value': 'Winners'},
            {'label': 'Runners-up', 'value': 'Runners-up'}
        ],
        value="Winners"
    ),
    dcc.Graph(id='choropleth_map'),
    
    html.Br(),

    html.Label('Select a World Cup Country:'),
    dcc.Dropdown(
        id='country_dropdown',
        options=[{'label': c, 'value': c} for c in sorted(world_cup['Winners'].unique())],
        value='Brazil'
    ),
    html.Div(id='country_win_output'),

    html.Br(),

    html.Label('Select a Year: '),
    dcc.Dropdown(
        id='year_dropdown',
        options=[{'label': y, 'value': y} for y in world_cup['Year']],
        value=1930
    ),
    html.Div(id='year_output')

])

@app.callback(
    Output('choropleth_map', 'figure'),
    Input('world_cup_dropdown', 'value'),
)
def update_map(selected_value):
    counts = world_cup[selected_value].value_counts().reset_index()
    counts.columns = ['Country', 'Count']

    fig = px.choropleth(
        counts,
        locations='Country',
        locationmode='country names',
        color='Count',
        color_continuous_scale="Plasma",
        title=f'World Cup {selected_value} and Total World Cup Wins'
    )
    return fig

@app.callback(
    Output('country_win_output', 'children'),
    Input('country_dropdown', 'value')
)

def update_country_win(selected_country):
    wins = (world_cup['Winners'] == selected_country).sum()
    return f'{selected_country} has won the World Cup {wins} times.'


@app.callback(
    Output('year_output', 'children'),
    Input('year_dropdown', 'value'),
)

def update_year_output(selected_year):
    r = world_cup[world_cup["Year"] == selected_year].iloc[0]
    return f'In {selected_year}, the World Cup winner was {r["Winners"]}, and the runner-up was {r["Runners-up"]}.'
 

if __name__ == '__main__':
    app.run_server(debug=True)
