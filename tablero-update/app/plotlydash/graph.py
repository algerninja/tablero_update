import plotly.express as px
import plotly.graph_objects as go

import random
import numpy as np
import pandas as pd

import pip._vendor.requests as requests


# Cargando data -- Luego se cambiara a la base de datos pero por ahora para
# mejor optimizacion a la hora de trabajar se usara un csv con los mismos datos de la base de datos
df = pd.read_csv('app/plotlydash/resultados.csv')

# Creamos 3 Columnas nuevas en el DF para simular a los indices
df['ig'] = np.random.randint(0, 10, len(df))
df['ip'] = np.random.randint(0, 10, len(df))
df['ie'] = np.random.randint(0, 10, len(df))


# Agrupamos todo por estados para luego sacar el promedio de los indices y pasarselos a la grafica de mapa
df_g = df.groupby('estado').mean()

# Traemos el geojson para asi manejar las coordenas y poder ubicar los puntos en el mapa
repo_url = "https://raw.githubusercontent.com/marcoah/info-geografica/master/geojson/vzla_division_pol.geojson"
geo_ve = requests.get(repo_url).json()


name_indice = ['Indice de Gestion',
               'Indice de Planificacion', 'Indice de Ejecucion']
available_indicators = ['ig', 'ip', 'ie']

indice = [{'label': i, 'value': j}
          for i, j in zip(name_indice, available_indicators)]

indice_institucion = [{'label': i, 'value': i}
                      for i in np.unique(df.loc[:, 'entidad/institucion'])]

# Funcion encargada de la creacion de los mapas segun el indice


def create_graph_map(yaxis_column_name, indice):

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
            family='Ubuntu',
            size=18,
            color='#7f7f7f'),

        annotations=[dict(
            x=0.55, y=0.1,
            xref='paper', yref='paper',
            text="",
            showarrow=False)])

    return fig


def create_graph_bar(df, list_select, data_bus_row, data_bus_col,
                     data_bus_col2=None, y_data_name=None,
                     x_data_name=None, bar_title=None,
                     orientacion_bar='v'):

    if data_bus_col2 == None:
        dff = df.loc[df[data_bus_row].isin(list_select),
                     [data_bus_row, data_bus_col]].groupby(
                         [data_bus_col]).count()
    else:
        dff = df.loc[df[data_bus_row].isin(list_select),
                     [data_bus_row, data_bus_col, data_bus_col2]].groupby(
                         [data_bus_col, data_bus_col2]).count()

    dff.reset_index(inplace=True)

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
            family='Ubuntu',
            size=12,
            color='#7f7f7f'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text="",
            showarrow=False
        )])

    return fig


def filter_dropdown_institucion(df, list_select):
    dff = df.loc[df['estado'].isin(list_select), ['entidad/institucion']].groupby(
        ['entidad/institucion']).count()

    dff = dff.reset_index()

    # dff['entidad/institucion'].unique()

    indice_institucion = [{'label': i, 'value': i} for i in np.unique(dff)]

    return indice_institucion, dff
