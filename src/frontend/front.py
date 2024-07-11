from dash import Dash, html, dcc, Input, Output, State, callback, no_update
import datetime
import os


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

customize_config = []
images_dict = {
    'human_bone': 'assets/configs/test/images/bone.png',
    'ArctinurusBoltoni': 'assets/configs/trilobites/images/ArctinurusBoltoni.png',
    'AturiaAlabamensis': 'assets/configs/trilobites/images/AturiaAlabamensis.png',
    'EurypterusRemipes': 'assets/configs/trilobites/images/EurypterusRemipes.png',
    'IsoletusMaximus': 'assets/configs/trilobites/images/IsoletusMaximus.png'
}

app.layout = html.Div(
    id='layout',
    children=[
        html.H4(
            id='header',
            children='FossilHunt',
            style={
                'font-size': '45px',
                'font-weight': 'bold',
                'margin-bottom': '30px',
                'position': 'absolute',
                'top': '100px',
                'left': '50%',
                'transform': 'translateX(-50%)'
            }
        ),
        html.Div(
            id='content-start',
            children=[
                html.Div(
                    dcc.Dropdown(
                        ['test', 'customize'],
                        'test',
                        id='model-dropdown',
                        clearable=False
                    ),
                    style = {'margin-bottom': '20px'}
                ),
                html.Div(
                    id='content-customize',
                    style = {'display' : 'none'},
                    children=[
                        html.Div(
                            children=[
                                html.H4('Customize Bones'),
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div('Os selectionne', style={'margin-right': '11px'}),
                                                dcc.Dropdown(
                                                    id='bone-name-dropdown',
                                                    options=[
                                                        {
                                                            'label': key,
                                                            'value': value
                                                        } for key, value in images_dict.items()
                                                    ],
                                                    placeholder='Select a bone',
                                                    clearable=False,
                                                    style={'width': '200px'}
                                                ),
                                            ],
                                            style = {'display': 'flex', 'flex-direction': 'row'}
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div('Rotation de l\'os', style={'margin-right': '5px'}),
                                                dcc.Input(
                                                    id='bone-rotation',
                                                    type='number',
                                                    min=0,
                                                    max=360,
                                                    step=5,
                                                    placeholder='Orientation',
                                                    value=45
                                                ),
                                            ],
                                            style = {'display': 'flex', 'flex-direction': 'row'}
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div('Echelle de l\'os', style={'margin-right': '15px'}),
                                                dcc.Input(
                                                    id='bone-scale',
                                                    type='number',
                                                    placeholder='Scale factor',
                                                    min=0,
                                                    max=2,
                                                    step=0.05,
                                                    value=0.5
                                                ),
                                            ],
                                            style = {'display': 'flex', 'flex-direction': 'row'}
                                        ),
                                html.Button(
                                    'Add Bone',
                                    id='add-bone-button',
                                    n_clicks=0
                                ),
                                html.Div(id='bone-list', children=[], style={'display': 'none'}),
                                html.Button(
                                    'Reset config',
                                    id='reset-bone-button',
                                    n_clicks=0
                                ),
                                html.Button(
                                    'Submit',
                                    id='submit-bone-list',
                                    n_clicks=0
                                ),
                                html.Div(id='dummy-output')
                                    ],
                                    style={'display': 'flex', 'flex-direction': 'column'}
                                ),
                            ],
                        ),
                    ]
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
                html.Div(
                    children=[],
                    id='model-name',
                    style = {'margin-bottom': '5px'}
                ),
                html.Div(
                    children=[],
                    id='time-elapsed',
                    style = {'margin-bottom': '20px'}
                ),
                html.Button(
                    'Finir la partie',
                    id='quit-button'
                ),
                html.Div(
                    children=0,
                    id='timer',
                    style={'display': 'none'}
                ),
            ],
            style = {'display': 'none'}
        ),


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
    Output('bone-list', 'children', allow_duplicate=True),
    Input('reset-bone-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_config(n_clicks):
    if n_clicks > 0:
        customize_config = []
        return html.Div()
    return no_update


@callback(
    Output('content-customize', component_property='style', allow_duplicate=True),
    Input('model-dropdown', 'value'),
    prevent_initial_call=True
)
def customize_bones(value):
    if value == 'customize':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output('bone-rotation', 'value'),
    Output('bone-scale', 'value'),
    Input('bone-name-dropdown', 'value')
)
def update_bone_fields(selected_bone_name):
    return 5, 0.5

@callback(
    Output('bone-list', 'children', allow_duplicate=True),
    Input('add-bone-button', 'n_clicks'),
    State('bone-name-dropdown', 'value'),
    State('bone-scale', 'value'),
    State('bone-rotation', 'value'),
    State('bone-list', 'children'),
    prevent_initial_call=True
)
def add_bone_to_list(n_clicks, path, scale, rotation, children):
    if n_clicks > 0:
        name = None
        for key, value in images_dict.items():
            if (value == path):
                name = key
        if (name is None):
            return no_update

        new_bone = {
            "name": name,
            "path": path,
            "scale_factor": scale,
            "rotation": rotation
        }
        customize_config.append(new_bone)
        children.append(html.Div(f"{name}, {path}, {scale}"))
        return children
    return no_update

@callback(
    Output('dummy-output', 'children'),  # Just a placeholder output
    Input('submit-bone-list', 'n_clicks'),
    State('bone-list', 'children'),
    prevent_initial_call=True
)
def submit_bone_list(n_clicks, bones):
    if n_clicks > 0:
        bone_data = [
            {
                "name": bones[i]['props']['children'].split(", ")[0],
                "path": bones[i]['props']['children'].split(", ")[1],
                "scale_factor": float(bones[i]['props']['children'].split(", ")[2])
            } for i in range(len(bones))
        ]
        # Send bone_data to backend
        # For demonstration, we just print it
        print(json.dumps(bone_data))
        return no_update
    return no_update


@callback(
    Output('content-start', component_property='style', allow_duplicate=True),
    Output('content-game', component_property='style', allow_duplicate=True),
    Output('model-name', 'children'),
    Output('time-elapsed', 'children', allow_duplicate=True),
    Output('timer', 'children', allow_duplicate=True),
    Input('start-button',  'n_clicks'),
    State('model-dropdown', 'value'),
    prevent_initial_call=True
)
def start_game(n_clicks, model):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}, f'Modèle : {model}', 'Temps écoulé : 0:00:00', 0
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
def quit_game(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}
    return no_update

if __name__ == '__main__':
    # app.run_server(debug=False, host="0.0.0.0", port=8050, use_reloader=False, dev_tools_ui=False)
    app.run()
