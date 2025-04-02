'''
Author: Abdulrahman Mahmoud
Date: April 1, 2025
URL: 
'''


import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv('assignment_7_data.csv')

df = df.replace({'West Germany': 'Germany'})

win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

win_counts['PlotLocation'] = win_counts['Country'].apply(
    lambda x: 'United Kingdom' if x == 'England' else x
)

fig = px.choropleth(
    win_counts,
    locations='PlotLocation',
    locationmode='country names',
    color='Wins',
    hover_name='Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    title='FIFA World Cup Wins by Country'
)

external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "FIFA World Cup Dashboard"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("FIFA World Cup Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(id='choropleth-map', figure=fig)
                ),
                className="mb-4"
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Countries that have won the World Cup")),
                dbc.CardBody(html.Ul(id='winner-list', className="list-unstyled"))
            ], className="mb-4"),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Country Win Count")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in win_counts['Country'].unique()],
                        placeholder="Select a country",
                        className="mb-2"
                    ),
                    html.Div(id='country-win-output')
                ])
            ], className="mb-4"),
            width=6
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("Match Details by Year")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                        placeholder="Select a year",
                        className="mb-2"
                    ),
                    html.Div(id='year-detail-output')
                ])
            ], className="mb-4"),
            width=12
        )
    ])
], fluid=True)

@app.callback(
    Output('country-win-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    if selected_country:
        wins = win_counts.loc[win_counts['Country'] == selected_country, 'Wins'].values[0]
        winning_years = df[df['Winner'] == selected_country]['Year'].unique()
        winning_years_sorted = sorted(winning_years)
        years_str = ", ".join(map(str, winning_years_sorted))
        return html.Div([
            html.P(f"{selected_country} has won the World Cup {wins} times.", className="text-success"),
            html.P(f"Years won: {years_str}.", className="text-secondary")
        ])
    return html.P("Select a country to see its win count and winning years.", className="text-muted")

@app.callback(
    Output('year-detail-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_details(selected_year):
    if selected_year:
        match = df[df['Year'] == selected_year].iloc[0]
        winner = match['Winner']
        runner_up = match['Runner-up']
        score = match['Score']
        venue = match['Venue']
        location = match['Location']
        attendance = match['Attendance']
        attendance_formatted = f"{int(attendance):,}"
        return html.P(
            f"In {selected_year}, {winner} won the World Cup with a score of {score} against {runner_up}. "
            f"The match was held at {venue} in {location} and was attended by {attendance_formatted} people.",
            className="text-info"
        )
    return html.P("Select a year to see the match details.", className="text-muted")

@app.callback(
    Output('winner-list', 'children'),
    Input('choropleth-map', 'figure')
)
def update_winner_list(_):
    sorted_win_counts = win_counts.sort_values(by='Wins', ascending=False)
    return [html.Li(f"{row['Country']}") for _, row in sorted_win_counts.iterrows()]

if __name__ == '__main__':
    app.run(debug=True)
