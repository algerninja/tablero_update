from dash import Dash, exceptions, callback_context
from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


import dash_daq as daq

# from .conexion_bd_pentaho import df_proyectos
from flask_login import current_user
from flask import session

from .graph import df, df_g, indice, indice_institucion, create_graph_bar, create_graph_map, filter_dropdown_institucion

import plotly.graph_objects as go


def init_dashboard(server):

    dash_app = Dash(server=server, url_base_pathname='/dash/', assets_external_path='app/plotlydash/assets',
                    external_stylesheets=[dbc.themes.BOOTSTRAP])

    dash_app.scripts.config.serve_locally = True

    search_bar = dbc.Row([
        html.Ul([
            html.Li(html.A(dbc.Row(
                dbc.Col(dbc.NavItem('Home', className='ml-2')), no_gutters=True),
                href='/home', className='nav-link'), className='nav-item active'),

            html.Li(html.A(dbc.Row(
                dbc.Col(dbc.NavItem('Dash', className='ml-2')), no_gutters=True),
                href='/dash', className='nav-link'), className='nav-item'),

            html.Li(html.A(
                dbc.Row(
                    dbc.Col(dbc.NavItem('Log In', className='ml-2')), no_gutters=True),
                href='/login', className='nav-link'), className='nav-item'),
            html.Li(html.A(
                dbc.Row(
                    dbc.Col(dbc.NavItem('Log Out', className='ml-2')), no_gutters=True),
                href='/logout', className='nav-link'), className='nav-item')
        ], className='navbar-nav')
    ])

    dash_app.title = 'Tableros'
    dash_app.layout = html.Div([
        dbc.Navbar([
            html.A(dbc.Row(dbc.Col(
                dbc.NavbarBrand("App name", className="ml-2")), no_gutters=True), href="/home"),

            dbc.NavbarToggler(id="navbar_toggler"),
            dbc.Collapse(search_bar, id="navbar_collapse", navbar=True),
        ], color="dark", dark=True
        ),

        html.Div(id='Content_Start', children=[
            # Selector de Indices Y boton para extender la informacion
            html.Div([dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='yaxis_column',
                        options=indice,
                        value='ig'), 
                        align="start", className="ml-5 col-md-9"),

                dbc.Col(
                    dbc.Button("Informacion por institucion", id='btn_more_info', n_clicks=0,
                        color="primary", ), className="col-md-2 text-right")
                    ])
                ]),

            # Graficos
            html.Div(children=[
                html.Div(
                    dcc.Graph(
                        id='Graph_Map',
                        selectedData={'points': [{'location': dict_aux} for dict_aux in df_g.index]})),

                html.Div(
                    dcc.Graph(
                        id='Graph_Bar'))

            ], style={
                'display': '-ms-grid',
                'display': 'grid',
                'grid-auto-columns': '1fr',
                '-ms-grid-columns': '1fr 1fr',
                'grid-template-columns': '1fr 1fr',
                '-ms-grid-rows': 'auto auto',
                'grid-template-rows': 'auto auto',
                'grid-row-gap': '16px',
                'grid-column-gap': '16px'}),

            html.Div(children=[dbc.Row([
                dbc.Col(
                    daq.Gauge(
                        id='Graph_Time_Ig',
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, df['ig'].mean()*0.5],
                                "yellow":[df['ig'].mean()*0.5, df['ig'].mean()],
                                "green":[df['ig'].mean(), df['ig'].max()]}},
                        showCurrentValue=True,
                        label='Indice de Gestion',
                        max=df['ig'].max(),
                        min=0,
                        value=df['ig'].mean()
                        ), width=2
                    ),

                dbc.Col(
                    daq.Gauge(
                        id='Graph_Time_V2',
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, df['ip'].mean()*0.5],
                                "yellow":[df['ip'].mean()*0.5, df['ip'].mean()],
                                "green":[df['ip'].mean(), df['ip'].max()]}},
                        showCurrentValue=True,
                        label='Indice de Planificacion',
                        max=df['ip'].max(),
                        min=0,
                        value=df['ip'].mean()
                        ), width=2
                    ),

                dbc.Col(
                    daq.Gauge(
                        id='Graph_Time_V3',
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, df['ie'].mean()*0.5],
                                "yellow":[df['ie'].mean()*0.5, df['ie'].mean()],
                                "green":[df['ie'].mean(), df['ie'].max()]}},
                        showCurrentValue=True,
                        label='Indice de Ejecucion',
                        max=df['ie'].max(),
                        min=0,
                        value=df['ie'].mean()
                        ), width=2
                    )
                ], justify="center")])
            ]),

        html.Div(id='Content_More_Info', children=[
            html.Div([dbc.Row([
                dbc.Col(dcc.Dropdown(id='dropdown_institucion',
                        options=indice_institucion
                        ), className='ml-5 col-md-9')])]),

            html.Div(dcc.Graph(id='Grahp_Bar_institucion'))
            ], style={'display': 'none'}),

        ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("navbar_collapse", "is_open"),
        [Input("navbar_toggler", "n_clicks")],
        [State("navbar_collapse", "is_open")])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @dash_app.callback(
        Output('Graph_Map', 'figure'),
        Input('yaxis_column', 'value'))
    def update_graph(yaxis_column_value):
        print(yaxis_column_value)

        fig = create_graph_map(yaxis_column_value, indice)

        return fig

    @dash_app.callback(
        [Output('Graph_Bar', 'figure'),
         Output('dropdown_institucion', 'options')],
        [Input('Graph_Map', 'selectedData')])
    def update_graph(selectedData):
        if selectedData is None:
            raise exceptions.PreventUpdate

        list_select = [dict_aux['location']
                       for dict_aux in selectedData['points']]

        fig_bar_1 = create_graph_bar(
            df=df, list_select=list_select, data_bus_row='estado', data_bus_col='estatus_proyecto', 
            y_data_name='proyectos', bar_title='Grafica de Estatus de proyectos')

        filter_dropdown = filter_dropdown_institucion(df, list_select)


        return fig_bar_1, filter_dropdown[0]
    @dash_app.callback(
        Output('Grahp_Bar_institucion', 'figure'),
        Input('dropdown_institucion', 'value'))
    def update_graph_institucion(value):
        fig_bar_institucion = create_graph_bar(
             df=df, list_select=[value], data_bus_row='entidad/institucion', data_bus_col='estatus_proyecto',
             x_data_name='institucion_estatus',
             orientacion_bar='h',
             bar_title='Graficos de barra Encargado de mostrar el estatus por institucion'
        )
        return fig_bar_institucion


    @dash_app.callback(
        Output('Content_More_Info', 'style'),
        [Input('btn_more_info', 'n_clicks')])
    def show_hide_element(visibility_state):

        if visibility_state % 2 == 0:
            return {'display': 'none'}
        else:
            return {'display': 'block'}
