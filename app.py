from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

df = pd.read_csv(r"https://raw.githubusercontent.com/danielukosz15/DashGamesProject/refs/heads/main/athlete_events.csv", sep=',')
df = df.dropna()
df['Games'] = df['City'] + ' '+ df['Year'].astype(str)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], title='Historia igrzysk by DL')
server = app.server

world_geo = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("Projekt z Wizualizacji Danych - Daniel Lukosz", className="ml-2", style={"marginLeft": 10})
                    ),
                ],
                align="center"
            )
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

MEDALS_MAP = [
    dbc.CardHeader(html.H5("Mapa ilości zdobytych medali na igrzyskach")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-medals_map",
                children=[
                    dbc.Row([
                        dbc.Col(html.P(["Wybierz igrzyska:"]), md=3),
                        dbc.Col([
                            dcc.Dropdown(
                                id="games-dropdown", 
                                clearable=False, 
                                style={"marginBottom": 50, "font-size": 16},
                                options=[
                                    {"label": i, "value": i}
                                    for i in df.sort_values('Year').Games.unique()
                                ],
                                value='Rio de Janeiro 2016'
                            ),
                        ], md=5),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='map',config={'displayModeBar': False}),
                        ]),
                    ]),
                    html.Div(id='output') 
                ]
            ),
        ]
    )
]

CLASS_BAR = [
    dbc.CardHeader(html.H5("Klasyfikacja medalowa wszechczasów")),
    dbc.Alert(
        "Not enough data to render these plots, please adjust the filters",
        id="no-data-alert",
        color="warning",
        style={"display": "none"},
    ),
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.P(["Wybierz ilość krajów z największą liczbą medali:"]), md=4),       
                                    dbc.Col(
                                        [
                                            daq.NumericInput(
                                                id='nocs_amount',
                                                min=1, max=100, value=10
                                            )
                                        ],
                                    md=5,
                                    ),
                                ],
                                style={"marginBottom": 10}
                            ),
                            
                            dcc.Tabs(
                                id="tabs",
                                value='Summer',
                                children=[
                                    dcc.Tab(
                                        label="Letnie",
                                        value='Summer',
                                        children=[
                                            dcc.Loading(
                                                id="loading-summer",
                                                children=[
                                                    dcc.Graph(
                                                            id="summer_class", config={'displayModeBar': False}
                                                        )
                                                    ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                    dcc.Tab(
                                        label="Zimowe",
                                        value='Winter',
                                        children=[
                                            dcc.Loading(
                                                id="loading-winter",
                                                children=[
                                                    dcc.Graph(
                                                            id="winter_class", config={'displayModeBar': False}
                                                        )
                                                ],
                                                type="default",
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            )
        ]
    ),
]

params = {'Age':'Wiek',
        'Weight':'Waga',
        'Height': 'Wzrost'}

ATHLETES_RANK = [
    dbc.CardHeader(html.H5("Parametry fizyczne zawodników w danej dyscyplinie")),
    dbc.CardBody(
        [               
            dbc.Row(
                [
                    dbc.Col(html.P(["Wybierz zakres czasowy:"]), md=4), 
                    html.Div(
                        dcc.RangeSlider(
                            id="year-slider",
                            min=df.Year.min(),
                            max=df.Year.max(),
                            step=2,
                            tooltip={"placement": "bottom", "always_visible": True},
                            marks=None,
                            allowCross=False,
                            value=[1970, 2016]
                            ),   
                        style={"marginBottom": 50}
                        ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.P(["Dyscyplina:"]), md=1),       
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="sport-dropdown", 
                                clearable=False, 
                                options=[
                                    {"label": i, "value": i}
                                    for i in df.sort_values('Sport').Sport.unique()
                                ],
                                value='Swimming'
                            ),
                        ],
                    md=5,
                    ),
                    dbc.Col(html.P(["Parametr:"]), md=1),       
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="param-dropdown", 
                                clearable=False, 
                                options=params,
                                value='Weight'
                            ),
                        ],
                    md=2,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dcc.Loading(
                        id="loading-distribution",
                        children=[
                            dcc.Graph(
                                    id="param_distribution", 
                                    config={'displayModeBar': False},
                                )
                            ],
                        type="default",
                    )
                ]
            )
        ]
    )
]

BEST_SPORTS = [
    dbc.CardHeader(html.H5("Dyscypliny, w których dany kraj zdobywa najwięcej medali")),
    dbc.CardBody(
        [   
            dbc.Row([
                    dbc.Col(html.P(["Wybierz kraj:"]), md=3),
                    dbc.Col([
                        dcc.Dropdown(
                            id="country_dropdown", 
                            clearable=False, 
                            style={"marginBottom": 50, "font-size": 16},
                            options=[
                                {"label": i, "value": i}
                                for i in df.sort_values('Team').Team.unique()
                            ],
                            value='Poland'
                            ),
                        ], 
                    md=5),
                    ]),
            dbc.Row(
                [    
                    dcc.Loading(
                        id="loading-best-sports",
                        children=[
                            dcc.Graph(
                                    id="country_piechart", 
                                    config={'displayModeBar': False},
                                )
                            ],
                        type="default",
                    )
                ]
            )
        ]
    )
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(MEDALS_MAP)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(CLASS_BAR)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(ATHLETES_RANK)),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(BEST_SPORTS)),], style={"marginTop": 30, "marginBottom": 30}),
    ],
    className="mt-12",
)

colors = {'Bronze':'brown',
        'Silver':'silver',
        'Gold': 'gold'}

translate = {'Bronze':'Brązowe',
        'Silver':'Srebrne',
        'Gold': 'Złote'}

@app.callback(
    Output('map','figure'),
    [Input('games-dropdown', 'value')]
)
def update_choropleth(games_val):
    medal_df = df.loc[(df.Games == games_val) & df.Medal.notnull()].groupby(["NOC"]).count()
    medal_df_index = medal_df.reset_index('NOC')
    world_geo = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    fig = px.choropleth(
        medal_df_index, geojson=world_geo, color="Medal", locations="NOC", featureidkey="id",
        color_continuous_scale="Oryel", labels={'Medal':'Zdobyte medale', 'NOC':'Kraj'},
        range_color=(np.min(medal_df_index["Medal"]), np.max(medal_df_index["Medal"]))
    )  
    fig.update_geos(showcountries=True, fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


@app.callback(
    Output('summer_class','figure'),
    [Input('nocs_amount', 'value')]
)
def plot_class_summer(NOCs_amount):
    class_df = df.loc[(df.Season == 'Summer')].groupby(["NOC", "Medal"]).count()
    class_df_index = class_df.reset_index(['NOC', 'Medal'])
    class_df_index = class_df_index.sort_values(by='ID', ascending=False,
               key=lambda x: class_df_index.groupby('NOC')['ID'].transform('sum'))

    bars = []
    for medal_color in ['Bronze', 'Silver', 'Gold']:
        medal_data = class_df_index[class_df_index['Medal'] == medal_color][:NOCs_amount]
        bar = go.Bar(name=translate[medal_color], x=medal_data['NOC'], 
                     y=medal_data['ID'], marker_color=colors[medal_color])
        bars.append(bar)

    fig = go.Figure(data=bars)

    sum_tmp = class_df_index.groupby('NOC').sum().reset_index().sort_values(by='ID', ascending=False)[:NOCs_amount]

    fig.add_trace(go.Scatter(
        x=sum_tmp["NOC"], 
        y=sum_tmp['ID'],
        text=sum_tmp['ID'],
        mode='text',
        textposition='top center',
        showlegend=False
        )
    )
    fig.update_layout(height=700, barmode='stack', xaxis_title="Kraj", yaxis_title="Zdobyte medale", legend_title='Kolor medalu')

    return fig

@app.callback(
    Output('winter_class','figure'),
    [Input('nocs_amount', 'value')]
)
def plot_class_winter(NOCs_amount):
    class_df = df.loc[(df.Season == 'Winter')].groupby(["NOC", "Medal"]).count()
    class_df_index = class_df.reset_index(['NOC', 'Medal'])
    class_df_index = class_df_index.sort_values(by='ID', ascending=False,
               key=lambda x: class_df_index.groupby('NOC')['ID'].transform('sum'))

    bars = []
    for medal_color in ['Bronze', 'Silver', 'Gold']:
        medal_data = class_df_index[class_df_index['Medal'] == medal_color][:NOCs_amount]
        bar = go.Bar(name=translate[medal_color], x=medal_data['NOC'], 
                     y=medal_data['ID'], marker_color=colors[medal_color])
        bars.append(bar)

    fig = go.Figure(data=bars)

    sum_tmp = class_df_index.groupby('NOC').sum().reset_index().sort_values(by='ID', ascending=False)[:NOCs_amount]

    fig.add_trace(go.Scatter(
        x=sum_tmp["NOC"], 
        y=sum_tmp['ID'],
        text=sum_tmp['ID'],
        mode='text',
        textposition='top center',
        showlegend=False
        )
    )
    fig.update_layout(height=700, barmode='stack', xaxis_title="Kraj", yaxis_title="Zdobyte medale", legend_title='Kolor medalu')

    return fig

@app.callback(
    Output('param_distribution','figure'),
    [Input('sport-dropdown', 'value'), Input('year-slider', 'value'), Input('param-dropdown', 'value')]
)
def update_sports_distribution(sport, year_range, param):
    sports_df = df.loc[(df.Sport == sport) & (df.Year.between(year_range[0], year_range[1]))]

    fig = ff.create_distplot([sports_df.loc[(sports_df.Sex == s)][param] for s in ['M', 'F']], ['Mężczyźni', 'Kobiety'], colors=['#42b0ff', '#e642ff'])

    fig.update_layout(legend_title='Płeć', xaxis_title=params[param])

    return fig

@app.callback(
    Output('country_piechart','figure'),
    [Input('country_dropdown', 'value')]
)
def update_piecharts(country):
    pie_df = df.loc[(df.Team == country) & df.Medal.notnull()].groupby(["Team", "Sport", "Season"]).count()
    pie_df_index = pie_df.reset_index()

    df_draw = pie_df_index.copy()
    df_draw.loc[(df_draw['ID'] / df_draw['ID'].sum()) < 0.01 , 'Sport'] = 'Inne'
    df_draw = df_draw.groupby(["Team", "Sport", "Season"])['ID'].sum().reset_index().sort_values('ID')


    reds_scale = pc.sample_colorscale(px.colors.sequential.Reds, samplepoints=20) 
    blues_scale = pc.sample_colorscale(px.colors.sequential.Blues, samplepoints=20)

    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    fig.add_trace(go.Pie(
        labels=df_draw[df_draw['Season'] == 'Summer']['Sport'].unique(), 
        values=df_draw[df_draw['Season'] == 'Summer']['ID'], 
        name="Igrzyska Letnie",
        marker=dict(colors=reds_scale)
        ),
              1, 1)
    
    fig.add_trace(go.Pie(
        labels=df_draw[df_draw['Season'] == 'Winter']['Sport'].unique(), 
        values=df_draw[df_draw['Season'] == 'Winter']['ID'], 
        name="Igrzyska Zimowe",
        marker=dict(colors=blues_scale)
        ),
              1, 2)

    fig.update_traces(hole=.4, textinfo='label+percent' , textposition='auto', insidetextorientation='radial')
    fig.update_layout(
        annotations=[dict(text='Letnie', x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
                        font_size=20, showarrow=False, xanchor="center"),
                    dict(text='Zimowe', x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
                        font_size=20, showarrow=False, xanchor="center")]
    )

    return fig

app.layout = html.Div(children=[NAVBAR, BODY])

if __name__ == '__main__':
    app.run(debug=True)
