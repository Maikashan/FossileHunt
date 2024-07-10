from dash import Dash, html, dcc, Input, Output, State, callback, no_update
import datetime


app = Dash(
    __name__,
    external_stylesheets=[
        'assets/style.css'
    ],
    title="FossilHunt",
    # suppress_callback_exceptions=True,
    prevent_initial_callbacks=True
)
server = app.server

app.layout = html.Div(
    id='layout',
    children=[
        html.H4(
            id='header',
            children='FossilHunt',
            style={'font-size': '45px', 'font-weight': 'bold', 'margin-bottom': '30px', 'position': 'absolute', 'top': '100px', 'left': '50%', 'transform': 'translateX(-50%)'}
        ),
        html.Div(
            id='content-start',
            children=[
                html.Div(
                    dcc.Dropdown(['test'], 'test', id='model-dropdown', clearable=False),
                    style = {'margin-bottom': '20px'}
                    ),
                html.Button(
                    'Commemcer le jeu',
                    id='start-button',
                    n_clicks =0
                    )
                ]
            ),
        html.Div(
            id='content-game',
            children=[
                dcc.Interval(
                    id='interval-component',
                    interval=1000,  # in milliseconds
                    n_intervals=0
                ),
                html.Div(children=[], id='model-name', style = {'margin-bottom': '5px'}),
                html.Div(children=[], id='nb-bone-found', style = {'margin-bottom': '5px'}),
                html.Div(children=[], id='time-elapsed', style = {'margin-bottom': '20px'}),
                html.Button(
                    'Finir la partie',
                    id='quit-button'
                ),
                html.Div(children=0, id='timer', style={'display': 'none'})
                ],
            style = {'display': 'none'}
            )
        ],
    style={
        'backgroundImage': 'url(/assets/background.png)',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'height': '100vh',
        'overflow': 'hidden',
        'display': 'flex',
        'flex-direction': 'column',
        'justify-content': 'center',
        'align-items': 'center',
    }
    )

@callback(
        Output('content-start', component_property='style', allow_duplicate=True),
        Output('content-game', component_property='style', allow_duplicate=True),
        Output('model-name', 'children'),
        Output('nb-bone-found', 'children'),
        Output('time-elapsed', 'children', allow_duplicate=True),
        Output('timer', 'children', allow_duplicate=True),
        Input('start-button',  'n_clicks'),
        State('model-dropdown', 'value'),
        prevent_initial_call=True
)
def start_game(n_clicks, model):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}, f'Modèle : {model}', 'Nombre d\'os trouvé(s) : 0', 'Temps écoulé : 0:00:00', 0
    return no_update

@callback(
    Output('time-elapsed', 'children', allow_duplicate=True),
    Output('timer', 'children', allow_duplicate=True),
    Input('interval-component', 'n_intervals'),
    State('timer', 'children'),
    prevent_initial_call=True
)
def update_time_elapsed(n_intervals, timer):
    if n_intervals:
        timer += 1
        return f'Temps écoulé : {datetime.timedelta(seconds=timer)}', timer
    return no_update

@callback(
        Output('content-game', component_property='style', allow_duplicate=True),
        Output('content-start', component_property='style', allow_duplicate=True),
        Input('quit-button',  'n_clicks'),
        prevent_initial_call=True
)
def restart_game(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}
    return no_update


if __name__ == '__main__':
    app.run(debug=True)
