import plotly.express as px
import plotly.graph_objects as go
import dash_html_components as html

import random
import numpy as np
import pandas as pd

import pip._vendor.requests as requests
import pyproj


# Cargando data -- Luego se cambiara a la base de datos pero por ahora para
# mejor optimizacion a la hora de trabajar se usara un csv con los mismos datos de la base de datos
df = pd.read_csv('app/plotlydash/resultados.csv')

# Creamos 3 Columnas nuevas en el DF para simular a los indices
df['ig'] = np.random.randint(0, 10, len(df))
df['ip'] = np.random.randint(0, 10, len(df))
df['ie'] = np.random.randint(0, 10, len(df))


# Agrupamos todo por estados para luego sacar el promedio de los indices y pasarselos a la grafica de mapa
df_g = df.groupby('estado').mean()
df_g = df_g.loc[:, ['ig', 'ip', 'ie']]

df_e = pd.DataFrame(data={
    'ig': df_g['ig'].min(),
    'ip': df_g['ip'].min(),
    'ie': df_g['ie'].min()},
    index={'Zona en Reclamación': 0})


df_g = pd.concat([df_g, df_e])

# Traemos el geojson para asi manejar las coordenas y poder ubicar los puntos en el mapa
repo_url = "https://raw.githubusercontent.com/marcoah/info-geografica/master/geojson/vzla_division_pol.geojson"
geo_ve = requests.get(repo_url).json()


# Creamos el nobmre de los indices
name_indice = ['Indice de Gestion',
               'Indice de Planificacion', 'Indice de Ejecucion']

# Creamos el valor de los indices
available_indicators = ['ig', 'ip', 'ie']

# Juntamos el nombre y el valor de los indices en un diccionario
indice = [{'label': i, 'value': j}
          for i, j in zip(name_indice, available_indicators)]

# Buscamos los valores unicos de las instituciones y
# lo guardamos en un diccionario
indice_institucion = [{'label': i, 'value': i}
                      for i in np.unique(df.loc[:, 'entidad/institucion'])]


# Funcion encargada de la creacion de los mapas segun el indice
def create_graph_map(yaxis_column_name, indice):

    # Se encarga asegurar que indice esta escojiendo el usuario
    if yaxis_column_name == 'ig':
        indice_nombre = 0
    elif yaxis_column_name == 'ip':
        indice_nombre = 1
    elif yaxis_column_name == 'ie':
        indice_nombre = 2

    # Pedimos que nos pasen el dato yaxis_column_name que es el nombre q poseera
    # la columna y este dato nos los da desde dash
    fig = px.choropleth(
        data_frame=df_g,
        geojson=geo_ve,
        locations=df_g.index,
        featureidkey='properties.estado',
        color_continuous_scale='Greens',
        color=df_g[yaxis_column_name],
        hover_name=df_g.index)

    fig.update_geos(showcountries=False, showcoastlines=False,
                    showland=False, fitbounds='locations')

    fig.update_layout(
        clickmode='event+select',
        title_text=f'Mapa de calor segun el {indice[indice_nombre]["label"]}',

        font=dict(
            family='Ubuntu', size=12,
            color='#7f7f7f'),

        annotations=[dict(
            x=0.55, y=0.1, xref='paper', yref='paper',
            text="", showarrow=False)]
    )

    return fig

# Funcion encargada de las creaciones de graficos de barra


def create_graph_bar(df, list_select, data_bus_row, data_bus_col,
                     data_bus_col2=None, y_data_name=None,
                     x_data_name=None, bar_title=None,
                     orientacion_bar='v'):


    # Nos aseguramos si el usuario agrego un dato para 2 columnas o
    # solo uno y buscamos los datos y agrupamos
    if data_bus_col2 == None:
        dff = df.loc[df[data_bus_row].isin(list_select),
                     [data_bus_row, data_bus_col]].groupby(
                         [data_bus_col]).count()
    else:
        dff = df.loc[df[data_bus_row].isin(list_select),
                     [data_bus_row, data_bus_col, data_bus_col2]].groupby(
                         [data_bus_col, data_bus_col2]).count()

    dff.reset_index(inplace=True)

    # Verificamos en que columna se desea trabajar ya sea la 'Y' o la 'X'
    if y_data_name == None:
        y_data = dff[data_bus_col]
    else:
        name = y_data_name
        x_data = data_bus_col
        y_data = y_data_name

    if x_data_name == None:
        x_data = dff[data_bus_col]
    else:
        name = x_data_name
        x_data = x_data_name
        y_data = data_bus_col

    dff.rename(columns={data_bus_row: name}, inplace=True)

    # Figura con Fx
    if data_bus_col2 == None:
        fig = px.bar(dff, y=y_data, x=x_data, text=name,
                     orientation=orientacion_bar)
    else:
        fig = px.bar(dff, y=y_data, x=x_data, text=name,
                     orientation=orientacion_bar, barmode='group',
                     color=data_bus_col2)

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        title_text=bar_title,

        font=dict(
            family='Ubuntu', size=12,
            color='#7f7f7f'),

        annotations=[dict(
            x=0.55, y=0.1, xref='paper', yref='paper',
            text="", showarrow=False)]
    )

    return fig


# Filtrado para las opciones de las instituciones
def filter_dropdown_institucion(df, list_select):
    dff = df.loc[df['estado'].isin(list_select), ['entidad/institucion']].groupby(
        ['entidad/institucion']).count()
    dff = dff.reset_index()

    indice_institucion = [{'label': i, 'value': i} for i in np.unique(dff)]

    return indice_institucion


# Generador de las listas/li automatis segun que institucion selecciones
def lista_proyectos(df, name_institucion, estatus_btn, compare):

    dff = df.loc[df['entidad/institucion'].isin([name_institucion])]
    dff = dff.loc[df['estatus_proyecto'].isin(estatus_btn)]
    dff = dff.reset_index(drop=True)

    x = []
    codigo = []
    if estatus_btn[0] in compare:
        for i in range(len(dff)):
            x.append(html.Div([
                html.Br(),
                html.Li(
                    html.A(id='hola', children=dff.loc[i, 'codigo_proyecto'],
                           href=dff.loc[i, 'codigo_proyecto']), style={'color': 'blue'}),
                html.Ul(
                    html.Div(html.Li(['Nombre: ', dff.loc[i, 'nombre_proyecto']]))),
                html.Ul(
                    html.Div(html.Li(['Estatus: ', dff.loc[i, 'estatus_proyecto']]))),
                html.Ul(
                    html.Div(html.Li(['Indice de gestion: ', dff.loc[i, 'ig']]))),
                html.Ul(
                    html.Div(html.Li(['Indice de planificacion: ', dff.loc[i, 'ip']]))),
                html.Ul(
                    html.Div(html.Li(['Indice de ejecucion: ', dff.loc[i, 'ie']])))
            ], className="ml-5 col-md-9"))
            codigo.append(dff.loc[i, 'codigo_proyecto'])
    else:
        x.append(html.Div([
            html.Br(),
            html.Li(html.A('Proyecto no encontrado'), style={'color': 'blue'}),
            html.Ul(
                html.Div(html.Li(['Nombre: ', 'Proyectos no encontrados'])))
        ], className="ml-5 col-md-9"))

    return x, codigo


def validar_datos_utm(data, variable_huso, variable_este, variable_norte, husos_validos=[18, 19, 20, 21], campo_clave='code'):
    '''
    Función que identifica las coordendas que son validas atendiendo a:
    1. Que las variables geograficas requeridas no tengan datos faltantes
    2. Que se encuentren en los husos que se requieren
    '''

    # -----------verificando los datos de las variables----------
    # verificando que sea un data frame
    try:
        data.head()
    except AttributeError:
        raise ValueError('Error en data')

    # verificando que las variables se encuentren dentro del data frame
    set_colunmas = set(data.columns)
    set_variables = set([variable_huso, variable_este, variable_norte])

    if not set_variables.issubset(set_colunmas):
        raise ValueError('Las variables no perteneces al data frame')

    # verificando que los husos sean numeros enteros
    try:
        husos_validos = [int(huso) for huso in husos_validos]
    except AttributeError:
        raise ValueError('Los usos debe ser enteros')

    # -----------Verificando datos validos----------

    # eliminando los elementos con NA
    data_geo = data.dropna(
        subset=[variable_huso, variable_este, variable_norte])

    # convirtiendo los datos de huso a int
    data_geo[variable_huso] = data_geo[variable_huso].astype('int')

    # descartando los husos que no corresponden a los husos validos
    data_geo = data_geo[data_geo[variable_huso].isin(husos_validos)]

    # ----extrayendo la data sin datos geograficos validos------

    # convirtiendo los codigos a conjuntos
    codigo_general = set(data[campo_clave].to_list())
    codigo_geo = set(data_geo[campo_clave].to_list())

    # obteniendo la diferencia de elementos del conjunto general al conjunto de registros con datos geograficos
    codigo_no_geo = codigo_general.difference(codigo_geo)

    # seleccionados los proyectos que no tienen los datos geograficos
    data_no_geo = data[data[campo_clave].isin(list(codigo_no_geo))]

    # ----Identificando la data sin datos geograficos validos------
    data_geo['datos_geograficos_validos'] = True
    data_no_geo['datos_geograficos_validos'] = False

    # ----Uniendo datas------
    data_resultado = pd.concat([data_geo, data_no_geo], ignore_index=True)

    return data_resultado


def transformar_utm_latlon(data, variable_huso, variable_este, variable_norte):
    '''
    Función que transforma las coordenas utm a coordenadas lat long desde un data frame creado con pandas
    '''

    # -----------verificando los datos de las variables----------
    # verificando que sea un data frame
    try:
        data.head()
    except AttributeError:
        raise ValueError('Error en data')

    # verificando que las variables se encuentren dentro del data frame
    set_colunmas = set(data.columns)
    set_variables = set([variable_huso, variable_este, variable_norte])

    if not set_variables.issubset(set_colunmas):
        raise ValueError('Las variables no perteneces al data frame')

    # -----------variables a utilizar----------
    # creando una lista con el nombre de las columnas
    nombre_columnas = data.columns.tolist()

    # agregando las variables lat y long
    nombre_columnas.extend(['lat', 'long'])

    # creando data frame vacio con el nombre de las columnas a utilizar
    df = pd.DataFrame(columns=nombre_columnas)

    # --------------------------------------------
    # ciclo según los husos
    for huso in data[variable_huso].unique():

        # Creamos el tranformador desde una proyeccion utm en el huso
        transproj = pyproj.Transformer.from_proj(
            {'proj': 'utm', 'zone': huso, 'ellps': 'WGS84', 'units': 'm'},
            {'proj': 'longlat', 'ellps': 'WGS84', 'datum': 'WGS84'},
            always_xy=True,
            skip_equivalent=True)

        # filtrando los proyectos segun el huso
        data_huso = data[data[variable_huso] == huso]

        # creamos una lista con tuplas (coordenada este, coordenada norte)
        coordenada_este_huso = data_huso[variable_este].tolist()
        coordenada_norte_huso = data_huso[variable_norte].tolist()

        # lista de coordenadas (se utilizara en el iterador)
        coordendas_huso = [tupla_coordenda for tupla_coordenda in zip(
            coordenada_este_huso, coordenada_norte_huso)]

        # creamos listas vacias para latitud y longitud
        lat_huso = []
        long_huso = []

        # iteramos sobre el resultado del transformador de coordendas
        for pt in transproj.itransform(coordendas_huso):

            # asignamos variables auxiliares
            long_i, lat_i = pt

            # agregamos a los vectors de latitud y longitud resultado
            lat_huso.append(lat_i)
            long_huso.append(long_i)

        # asignamos resultado de lat y long por huso
        data_huso['lat'] = lat_huso
        data_huso['long'] = long_huso

        # creando df final
        df = pd.concat([df, data_huso], ignore_index=True)

    return df
