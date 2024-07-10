from dash import Dash, html, dcc, Input, Output, State, callback, no_update


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
        ),
        html.Div(
            id='content-start',
            children=[
                html.Div(
                    dcc.Dropdown(['test'], 'test', id='model-dropdown')
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
                html.Div(children=[], id='model-name'),
                html.Button(
                    'Recommencer la partie',
                    id='restart-button'
                    )
                ]
            )
        ],
    )

@callback(
        Output('content-start', component_property='style', allow_duplicate=True),
        Output('content-game', component_property='style', allow_duplicate=True),
        Output('model-name', 'children'),
        Input('start-button',  'n_clicks'),
        State('model-dropdown', 'value'),
        prevent_initial_call=True
)
def start_game(n_clicks, model):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}, model
    return no_update

@callback(
        Output('content-game', component_property='style', allow_duplicate=True),
        Output('content-start', component_property='style', allow_duplicate=True),
        Input('restart-button',  'n_clicks'),
        prevent_initial_call=True
)
def restart_game(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}
    return no_update
    

if __name__ == '__main__':
    app.run(debug=True)
