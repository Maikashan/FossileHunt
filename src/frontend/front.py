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

#bones_data = os.path.join(os.getcwd(), 'config.json')
bones_data = {
    "os": [
        {
            "name": "human_bone",
            "path": "assets/configs/test/images/bone.png",
            "scale_factor": 0.05
        },
        {
            "name": "dino_bone",
            "path": "assets/configs/test/images/dino_bone.png",
            "scale_factor": 0.1
        }
    ]
}

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
                    dcc.Dropdown(['test', 'customize'], 'test', id='model-dropdown', clearable=False),
                    style = {'margin-bottom': '20px'}
                    ),
                    html.Div(
            id='content-customize',
            style = {'display' : 'none'}, 
            #style={'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'background': 'white', 'padding': '20px', 'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)'},
            children=[
                html.Div(
                    children=[
                        html.H4('Customize Bones'),
                        dcc.Dropdown(
                            id='bone-name-dropdown',
                            options=[{'label': bone['name'], 'value': bone['name']} for bone in bones_data['os']],
                            placeholder='Select a bone'
                        ),
                        dcc.Input(
                            id='orientation',
                            type='number',
                            min=0,
                            max=360,
                            step=5,
                            placeholder='Orientation',
                            value=45
                        ),
                        dcc.Input(
                            id='bone-scale',
                            type='number',
                            placeholder='Scale factor',
                            min=0,
                            max=2,
                            step=0.05,
                            value=0.5
                        ),
                        html.Button(
                            'Add Bone',
                            id='add-bone-button',
                            n_clicks=0
                        ),
                        html.Div(id='bone-list', children=[]),
                        html.Button(
                            'Submit',
                            id='submit-bone-list',
                            n_clicks=0
                        ),
                        html.Div(id='dummy-output')
                    ]
                )
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
                html.Div(children=[], id='model-name', style = {'margin-bottom': '5px'}),
                html.Div(children=[], id='nb-bone-found', style = {'margin-bottom': '5px'}),
                html.Div(children=[], id='time-elapsed', style = {'margin-bottom': '20px'}),
                html.Button(
                    'Finir la partie',
                    id='quit-button'
                ),
                html.Div(children=0, id='timer', style={'display': 'none'}),
                html.Div(children=0, id='bone-count', style={'display': 'none'}),
                html.Button(
                    id='bone-button',
                    n_clicks=0,
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
    [Output('bone-path', 'value'), Output('bone-scale', 'value')],
    Input('bone-name-dropdown', 'value')
)
def update_bone_fields(selected_bone_name):
    if selected_bone_name:
        bone = next(bone for bone in bones_data['os'] if bone['name'] == selected_bone_name)
        return bone['path'], bone['scale_factor']
    return '', 0.5

@callback(
    Output('bone-list', 'children'),
    Input('add-bone-button', 'n_clicks'),
    State('bone-name-dropdown', 'value'),
    State('bone-path', 'value'),
    State('bone-scale', 'value'),
    State('bone-list', 'children'),
    prevent_initial_call=True
)
def add_bone_to_list(n_clicks, name, path, scale, children):
    if n_clicks > 0:
        new_bone = {
            "name": name,
            "path": path,
            "scale_factor": scale
        }
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
    Output('nb-bone-found', 'children', allow_duplicate=True),
    Output('time-elapsed', 'children', allow_duplicate=True),
    Output('timer', 'children', allow_duplicate=True),
    Output('bone-count', 'children', allow_duplicate=True),
    Input('start-button',  'n_clicks'),
    State('model-dropdown', 'value'),
    prevent_initial_call=True
)
def start_game(n_clicks, model):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}, f'Modèle : {model}', 'Nombre d\'os trouvé(s) : 0', 'Temps écoulé : 0:00:00', 0, 0
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

@callback(
    Output('nb-bone-found', 'children', allow_duplicate=True),
    Output('bone-count', 'children', allow_duplicate=True),
    Input('bone-button', 'n_clicks'),
    State('bone-count', 'children'),
    prevent_initial_call=True
)
def update_bone_count(n_clicks, bone_count):
    if n_clicks > 0:
        bone_count += 1
        return f'Nombre d\'os trouvé(s) : {bone_count}', bone_count
    return no_update

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8050, use_reloader=False, dev_tools_ui=False)
