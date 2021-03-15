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

from .graph import df, df_g, indice, indice_institucion
from .graph import create_graph_bar, create_graph_map
from .graph import filter_dropdown_institucion, lista_proyectos, validar_datos_utm, transformar_utm_latlon

import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import numpy as np


page_1 = html.Div([
    # Contenedor que mostrata los datos a nivel nacional
    html.Div(id='Content_Start', children=[
        html.Br(),
        html.Div(html.H2('Indice de gestion nacional'),
                 className="md-5 text-center"),

        # Selector de Indices Y boton para extender la informacion
        html.Div([dbc.Row([
            dbc.Col(dcc.Dropdown(
                    id='yaxis_column',
                    options=indice,
                    value='ig'),
                    align="start", className="ml-5 col-md-9"),

            dbc.Col(dbc.Button("Informacion por institucion",
                               id='btn_more_info', n_clicks=0,
                               color="primary", ), className="col-md-2 text-right")
        ])]),

        # Graficos
        html.Div(children=[
            # Grafico de Mapa a nivel nacional
            html.Div(dcc.Graph(
                id='Graph_Map',
                selectedData={'points': [{'location': dict_aux} for dict_aux in df_g.index]}),
                className="ml-5 col-md-10"),

            # Grafico de Barra mostrando el estatus a nivel nacional
            html.Div(dcc.Graph(
                id='Graph_Bar'),
                className="mr-2 col-md-10")

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

        # Graficos del relog que muestran el indice a nivel nacional
        html.Div(children=[dbc.Row([
            # Grafico de relog del indice de gestion
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
                    min=0
                ), width=2, className="col-sm-2"
            ),

            # Grafico de relog del indice de planificacion
            dbc.Col(
                daq.Gauge(
                    id='Graph_Time_Ip',
                    color={
                        "gradient": True,
                        "ranges": {
                            "red": [0, df['ip'].mean()*0.5],
                            "yellow":[df['ip'].mean()*0.5, df['ip'].mean()],
                            "green":[df['ip'].mean(), df['ip'].max()]}},
                    showCurrentValue=True,
                    label='Indice de Planificacion',
                    max=df['ip'].max(),
                    min=0
                ), width=2, className="col-sm-2"
            ),

            # Grafico de relog del indice de ejecucion
            dbc.Col(
                daq.Gauge(
                    id='Graph_Time_Ie',
                    color={
                        "gradient": True,
                        "ranges": {
                            "red": [0, df['ie'].mean()*0.5],
                            "yellow":[df['ie'].mean()*0.5, df['ie'].mean()],
                            "green":[df['ie'].mean(), df['ie'].max()]}},
                    showCurrentValue=True,
                    label='Indice de Ejecucion',
                    max=df['ie'].max(),
                    min=0
                ), width=2, className="col-sm-2"
            )
        ], justify="center")])
    ], style={'display': 'block'}),

    # Contenedor encargado de mostrar las intictuciones segun el estado o
    # los estados
    html.Div(id='Content_More_Info', children=[
        html.Div(html.H2('Indice de gestion por institucion'),
                 className="md-5 text-center"),

        html.Div([dbc.Row([
            dbc.Col(dcc.Dropdown(id='dropdown_institucion',
                                 options=indice_institucion
                                 ), className="ml-5 col-md-9"),
            dbc.Col(dbc.Button("Ver Proyectos", id='btn', n_clicks=0,
                               color="primary"), className="md-5 text-center")])
                  ]),

        html.Div([
            html.Div(dcc.Graph(id='Grahp_Bar_institucion'),
                     className="ml-5 col-md-10"),
            html.Div(dcc.Graph(id='Graph_Bar_Categories'),
                     className="mr-2 col-md-10")
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
                    id='Grafico_reloj_rosaig',
                    color={
                        "gradient": True,
                        "ranges": {
                            "red": [0, 20],
                            "yellow":[20, 80],
                            "green":[80, 100]}},
                    showCurrentValue=True,
                    label='Entidad_Institucion',
                    max=100,
                    min=0,
                    value=8,
                ), width=2, className="col-sm-2"
            ),
            dbc.Col(
                daq.Gauge(
                    id='grafico_reloj_rosaip',
                    color={
                        "gradient": True,
                        "ranges": {
                            "red": [0, 20],
                            "yellow":[20, 80],
                            "green":[80, 100]}},
                    showCurrentValue=True,
                    label='Entidad_Institucion',
                    max=100,
                    min=0,
                    value=8,
                ), width=5, className="col-sm-2"
            ),
            dbc.Col(
                daq.Gauge(
                    id='grafico_reloj_rosaie',
                    color={
                        "gradient": True,
                        "ranges": {
                            "red": [0, 20],
                            "yellow":[20, 80],
                            "green":[80, 100]}},
                    showCurrentValue=True,
                    label='Entidad_Institucion',
                    max=100,
                    min=0,
                    value=8,
                ), width=5, className="col-sm-2"
            )
        ], justify="center")]),

        html.Div(dcc.Graph(id='Grahp_Map_multipoints'), className='ml-3 mr-3')
    ]),

    # Contenedor que se encarga de mostrar los proyectos segun la institucion seleccionada
    html.Div(id='Content_View_Projects', children=[
        html.Div(html.H2('Proyecto por institucion'),
                 className="md-5 text-center"),

        # Botones para seleccionar que estado desea mostrar del proyecto
        html.Div([dbc.ButtonGroup([
            dbc.Button('All', id='btn_select_all',
                       n_clicks=0, color="primary"),
            dbc.Button('Ejecución', id='btn_select_Ejec',
                       n_clicks=0, color="primary"),
            dbc.Button('Culminado', id='btn_select_Cul',
                       n_clicks=0, color="primary"),
            dbc.Button('Cancelado por institucion',
                       id='btn_select_CxI', n_clicks=0, color="primary"),
            dbc.Button('Espera Desembolso', id='btn_select_EDes',
                       n_clicks=0, color="primary"),
            dbc.Button('Aprobado', id='btn_select_Apr',
                       n_clicks=0, color="primary")
        ])], className="md-5 text-center"),

        # Mostrar la lista de projector
        html.Ul(id='List_Project'),
    ], style={'display': 'none'})])


def page_2(text):
    text = text[6:]
    codigo = df['codigo_proyecto'].tolist()
    codigo = set(codigo)

    if text in codigo:
        dff = df.loc[df['codigo_proyecto'] == text, ]
        dff = dff.reset_index()

        kl = dt.datetime.strptime(dff.loc[0, 'fecha_inicio'], '%d/%m/%Y')
        k = kl + dt.timedelta(dff.loc[0, 'duracion_proyecto'] * 30)

        lol = go.Figure(data=[go.Scatter(x=[kl, k], y=[2, 4, 6, 8, 10])])

        lol.update_layout(
            title_text=f'Linea de tiempo del proyecto {text}',
            xaxis_range=[kl - dt.timedelta(7),
                         k + dt.timedelta(7)],
            margin={"r": 25, "t": 25, "l": 25, "b": 25}
        )

        validate = validar_datos_utm(
            dff, 'huso_id_name', 'coord_este', 'coord_norte', campo_clave='codigo_proyecto')

        latlong = transformar_utm_latlon(
            validate, 'huso_id_name', 'coord_este', 'coord_norte')

        fig_map = go.Figure(go.Scattermapbox(
            lat=latlong['lat'],
            lon=latlong['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=30
            ),
            text=latlong['codigo_proyecto'],
        ))

        fig_map.update_layout(
            title_text=f'Ubicacion del proyecto {text}',
            mapbox_style="mapbox://styles/algerninja/ckm5ak8pa3l3418qt1cgj39vz",
            margin={"r": 25, "t": 25, "l": 25, "b": 25},
            hovermode='closest',
            mapbox=dict(
                accesstoken="pk.eyJ1IjoiYWxnZXJuaW5qYSIsImEiOiJja201YWoxaTIwY2hlMndzM2l4NjQxd2ZqIn0.wTI7UCNELi0sdiLHu8LmcA",
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=latlong.loc[0, 'lat'],
                    lon=latlong.loc[0, 'long'],
                ),
                pitch=0,
                zoom=15
            )
        )

        x = html.Div([
            html.Br(),
            html.H2(f'Informacion de {text}',
                    className='ml-5 text-center'),

            html.Div(children=[dbc.Row([
                # Grafico de relog del indice de gestion
                dbc.Col(
                    daq.Gauge(
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, 4],
                                "yellow":[4, 6],
                                "green":[6, 10]}},
                        showCurrentValue=True,
                        label='Indice de Gestion',
                        max=10,
                        min=0,
                        value=dff.loc[0, 'ig']
                    ), width=2, className="col-sm-2"
                ),

                # Grafico de relog del indice de planificacion
                dbc.Col(
                    daq.Gauge(
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, 4],
                                "yellow":[4, 6],
                                "green":[6, 10]}},
                        showCurrentValue=True,
                        label='Indice de Planificacion',
                        max=10,
                        min=0,
                        value=dff.loc[0, 'ip']
                    ), width=2, className="col-sm-2"
                ),

                # Grafico de relog del indice de ejecucion
                dbc.Col(
                    daq.Gauge(
                        color={
                            "gradient": True,
                            "ranges": {
                                "red": [0, 4],
                                "yellow":[4, 6],
                                "green":[6, 10]}},
                        showCurrentValue=True,
                        label='Indice de Ejecucion',
                        max=10,
                        min=0,
                        value=dff.loc[0, 'ie']
                    ), width=2, className="col-sm-2"
                )
            ], justify="center")]),

            html.Div([]),

            html.Div([dbc.Row([
                dbc.Col(
                    html.Div(dcc.Graph(figure=lol),
                             className='ml-4 mr-4')
                ),
                dbc.Col(
                    html.Div(dcc.Graph(figure=fig_map),
                             className='ml-4 mr-4')
                )
            ])]),
        ])
    return x


def init_dashboard(server):

    dash_app = Dash(server=server, url_base_pathname='/dash/',
                    external_stylesheets=[dbc.themes.BOOTSTRAP])

    dash_app.scripts.config.serve_locally = True

    # Creacion del Narvar/Barra de navegacion
    search_bar = dbc.Row([html.Ul([
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
    ], className='navbar-nav')])

    # Titulo de la pagina --Provicionalmente esta como Tablero
    dash_app.title = 'Tableros'  # Nombre dispuesto a cambio

    dash_app.layout = html.Div([
        dbc.Navbar([
            html.A(dbc.Row(dbc.Col(
                dbc.NavbarBrand("App name", className="ml-2")), no_gutters=True), href="/home"),

            dbc.NavbarToggler(id="navbar_toggler"),
            dbc.Collapse(search_bar, id="navbar_collapse", navbar=True),
        ], color="dark", dark=True
        ),

        dcc.Location(id='url', refresh=False),

        html.Div(id='page-content'),
    ])

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    # Despliegue de el navbar/ barra de busqueda
    @ dash_app.callback(
        Output("navbar_collapse", "is_open"),
        [Input("navbar_toggler", "n_clicks")],
        [State("navbar_collapse", "is_open")])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Modificacion del mapa segun el indice
    @ dash_app.callback(
        Output('Graph_Map', 'figure'),
        Input('yaxis_column', 'value'))
    def update_graph(yaxis_column_value):

        fig = create_graph_map(yaxis_column_value, indice)

        return fig

    # Actualizacion del las opciones de dropdown, grafico de barras y relojes
    @ dash_app.callback(
        [Output('Graph_Bar', 'figure'),
         # Actualizacion de las opciones que usaran en el dropdown
         Output('dropdown_institucion', 'options'),
         # Actulizacion de los graficos de relog
         Output('Graph_Time_Ig', 'value'),
         Output('Graph_Time_Ip', 'value'),
         Output('Graph_Time_Ie', 'value')],
        [Input('Graph_Map', 'selectedData')])
    def update_graph(selectedData):
        if selectedData is None:
            raise exceptions.PreventUpdate

        # Se encarga de buscar la locaciones/estados indicado en el
        # mapa de indice nacional
        list_select = [dict_aux['location']
                       for dict_aux in selectedData['points']]

        # Creacion de el grafico de barras segun el locaciones/estados seleccionado
        fig_bar_1 = create_graph_bar(
            df=df, list_select=list_select, data_bus_row='estado', data_bus_col='estatus_proyecto',
            y_data_name='proyectos', bar_title='Grafica de Estatus de proyectos')

        # Modificacion de las opciones a seleccionar segun que locaciones/estados
        # selecciones en el mapa
        filter_dropdown = filter_dropdown_institucion(df, list_select)

        # Actualizacion de los graficos de relog segun el mapa
        v_ig = df.loc[df['estado'].isin(list_select), ['estado', 'ig']].mean()

        v_ip = df.loc[df['estado'].isin(list_select), ['estado', 'ip']].mean()

        v_ie = df.loc[df['estado'].isin(list_select), ['estado', 'ie']].mean()

        return fig_bar_1, filter_dropdown, round(v_ig[0], 2), round(v_ip[0], 2), round(v_ie[0], 2)

    # Actualizacion de grafico de barrar por el estatus de la institucion
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

    # Actualizacion de grafico de barrar por la categoria de la institucion
    @dash_app.callback(
        Output('Graph_Bar_Categories', 'figure'),
        Input('dropdown_institucion', 'value'))
    def update_graph_institucion(value):
        fig_bar_cartegoria = create_graph_bar(
            df=df, list_select=[value], data_bus_row='entidad/institucion', data_bus_col='categoria',
            x_data_name='institucion_categoria',
            orientacion_bar='h',
            bar_title='Graficos de barra Encargado de mostrar la categoria por institucion'
        )
        return fig_bar_cartegoria

    # Ocultar o mostrar el contenedor del indice por intitucion

    @ dash_app.callback(
        Output('Content_More_Info', 'style'),
        [Input('btn_more_info', 'n_clicks')])
    def show_hide_element(btn_institucion):
        if btn_institucion % 2 == 0:
            return {'display': 'none'}
        else:
            return {'display': 'block'}

    # Selector de estatus del proyecto
    @ dash_app.callback(
        Output('List_Project', 'children'),
        [Input('dropdown_institucion', 'value'),
         Input('btn_select_all', 'n_clicks'),
         Input('btn_select_Ejec', 'n_clicks'),
         Input('btn_select_Cul', 'n_clicks'),
         Input('btn_select_CxI', 'n_clicks'),
         Input('btn_select_EDes', 'n_clicks'),
         Input('btn_select_Apr', 'n_clicks')
         ])
    def update_output_div(input_value, btn1, btn2, btn3, btn4, btn5, btn6):

        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'btn_select_all' in changed_id:
            btn_option = ['Ejecución', 'Culminado',
                          'cancelado_institucion', 'Espera Desembolso', 'Aprobado']
        elif 'btn_select_Ejec' in changed_id:
            btn_option = ['Ejecución']
        elif 'btn_select_Cul' in changed_id:
            btn_option = ['Culminado']
        elif 'btn_select_CxI' in changed_id:
            btn_option = ['cancelado_institucion']
        elif 'btn_select_EDes' in changed_id:
            btn_option = ['Espera Desembolso']
        elif 'btn_select_Apr' in changed_id:
            btn_option = ['Aprobado']
        else:
            btn_option = ['Ejecución', 'Culminado',
                          'cancelado_institucion', 'Espera Desembolso', 'Aprobado']

        dff = df.loc[df['entidad/institucion'].isin(
            [input_value]), ['estatus_proyecto']]
        x = dff['estatus_proyecto'].tolist()
        x = set(x)

        return lista_proyectos(df, input_value, btn_option, compare=x)[0]

    @dash_app.callback(
        [Output('btn_select_all', 'color'),
         Output('btn_select_Ejec', 'color'),
         Output('btn_select_Cul', 'color'),
         Output('btn_select_CxI', 'color'),
         Output('btn_select_EDes', 'color'),
         Output('btn_select_Apr', 'color')],
        Input('dropdown_institucion', 'value'))
    def colorboton(valor):
        dff = df.loc[df['entidad/institucion']
                     .isin([valor]), ['estatus_proyecto']]
        estatus = dff['estatus_proyecto'].tolist()
        estatus = set(estatus)

        btn1 = 'primary'
        btn2 = 'primary' if 'Ejecución' in estatus else 'secondary'
        btn3 = 'primary' if 'Culminado' in estatus else 'secondary'
        btn4 = 'primary' if 'cancelado_institucion' in estatus else 'secondary'
        btn5 = 'primary' if 'Espera Desembolso' in estatus else 'secondary'
        btn6 = 'primary' if 'Aprobado' in estatus else 'secondary'

        return btn1, btn2, btn3, btn4, btn5, btn6

    # Ocultar el contenedor de los proyectos
    @ dash_app.callback(
        Output('Content_View_Projects', 'style'),
        [Input('btn', 'n_clicks')])
    def show_hide_element(btn_proyecto):

        if btn_proyecto % 2 == 0:
            return {'display': 'none'}
        else:
            return {'display': 'block'}

    @dash_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/dash/':
            return page_1
        elif pathname != '/dash/':
            return page_2(pathname)
        else:
            return page_1

    @dash_app.callback(
        Output('Grahp_Map_multipoints', 'figure'),
        Input('dropdown_institucion', 'value'))
    def update_graph_multipoints(value):

        dff = df.loc[df['entidad/institucion'] == value, :]
        validate = validar_datos_utm(
            dff, 'huso_id_name', 'coord_este', 'coord_norte', campo_clave='codigo_proyecto')

        latlong = transformar_utm_latlon(
            validate, 'huso_id_name', 'coord_este', 'coord_norte')
        multipuntos = go.Figure(go.Scattermapbox(
            lat=latlong['lat'],
            lon=latlong['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=latlong['codigo_proyecto'],
        ))

        multipuntos.update_layout(
            mapbox_style="mapbox://styles/algerninja/ckm5ak8pa3l3418qt1cgj39vz",
            margin={"r": 25, "t": 25, "l": 25, "b": 25},
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiYWxnZXJuaW5qYSIsImEiOiJja201YWoxaTIwY2hlMndzM2l4NjQxd2ZqIn0.wTI7UCNELi0sdiLHu8LmcA',
                bearing=0,
                center=dict(
                    lat=6.561958,
                    lon=-64.584106
                ),
                pitch=0,
                zoom=4.5
            ),
        )
        return multipuntos

    @dash_app.callback(
        Output('Container_institucion', 'style'),
        Input('dropdown_institucion', 'value'))
    def show_graph_institucion(value):

        if value == None:
            return {'display': 'none'}
        else:
            return {'display': 'block'}
