import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import numpy as np

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        SystemExit()
    print("Connection successful")
    return conn

def get_query(conn,sql):
    try:
        df = sqlio.read_sql_query(sql, conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        return 1
    return df

#datos de acceso a la db
datos_acceso = {
    'host' : '190.202.145.229',
    'port' : '3538',
    'dbname' : 'dw_fci',
    'user' : 'consulta',
    'password' : 'consulta'
    }



####################################
#PROYECTOS
#trayendo los datos

#conectando a base de datos
conn = connect(datos_acceso)

#realizando la sentencia sql de busqueda de los proyectos 'Ejecución', 'Culminado', 'cancelado_institucion','Espera Desembolso', 'Aprobado' de la base de la tabla fi_proyectos
sql = '''
SELECT id_entidad,  \"entidad/institucion\", rif, tipo_institucion,id_proyecto_o, codigo_proyecto, nombre_proyecto, descripcion_proyecto, estatus_proyecto, fecha_inicio, año, tipo_sector, categoria_general, categoria, subcategoria, fecha_creacion, redi, estado, municipio, parroquia, coord_norte, coord_este, huso_id_name, duracion_proyecto, monto_proyecto, monto_desembolso, monto_utilizado, avance_financiero, avance_fisico, tipo_proyecto, proyecto_marco, nombre_proyecto_marco, esquema_desembolso, cantidad_rendiciones, cantidad_avances 
FROM fi_proyectos 
WHERE estatus_proyecto in ('Ejecución', 'Culminado', 'cancelado_institucion','Espera Desembolso', 'Aprobado')
'''

#realizando la consulta
df_proyectos = get_query(conn, sql)

#cerrando conexion
conn = None

#transformado datos a float
df_proyectos['coord_norte'] = df_proyectos['coord_norte'].astype('float')
df_proyectos['coord_este'] = df_proyectos['coord_este'].astype('float')
df_proyectos['huso_id_name'] = df_proyectos['huso_id_name'].astype('float')
df_proyectos['id_proyecto_o'] = df_proyectos['id_proyecto_o'].astype('float')
df_proyectos['duracion_proyecto'] = df_proyectos['duracion_proyecto'].astype('float')



