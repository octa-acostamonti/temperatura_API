import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#Carga y Tratamiento de los datos
temp=pd.read_csv('temperatura_NY.csv')
df=pd.DataFrame(temp) 

if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Convertir la columna "time" a tipo datetime
df['time'] = pd.to_datetime(df['time'])

# Establecer la columna "time" como índice del DataFrame
df.set_index('time', inplace=True)

# Obtener los valores mínimos y máximos de las fechas
fecha_min = df.index.min().date()
fecha_max = df.index.max().date()


st.title('Proyecto Grupal: Línea Temporal de Temperatura en Nueva York')
# Crear la aplicación de Streamlit
st.markdown(" ### Gráfica de Temperatura en Nueva York")
st.markdown('***')
st.markdown('Consultora Veloxia')
st.markdown('* Se muestra a continuación una gráfica de temperatura de acuerdo a fecha en la ciudad de Nueva York.')
st.markdown('* Es importante recalcar que la información es extraída de la API del clima de Nueva York, misma que tiene un retraso de 5 días (aproximadamente) para la disposición de los datos.')
st.markdown('* Las fechas disponibles están marcadas por defecto son:')
st.write('Fecha mínima disponible: ', fecha_min, fontsize=35)
st.write('Fecha máxima disponible: ', fecha_max, fontsize=35)

st.markdown('* Los datos están automatizados mediante Airflow permitiendo la descarga y disponibilización de los datos en la gráfica y dataframe mostrado.')

st.markdown('***')


# Crear los controles de selección de fechas utilizando una barra deslizante
fecha_inicio = st.slider("Fecha de inicio", min_value=fecha_min, max_value=fecha_max, value=fecha_min)
fecha_fin = st.slider("Fecha de fin", min_value=fecha_min, max_value=fecha_max, value=fecha_max)

# Validar las fechas seleccionadas
if fecha_inicio > fecha_fin:
    st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
else:
    # Filtrar el dataframe basado en las fechas seleccionadas
    df_filtrado = df[(df.index >= pd.to_datetime(fecha_inicio)) & (df.index <= pd.to_datetime(fecha_fin))]

    # Resamplear los datos a una muestra mensual
    df_resampled = df_filtrado.resample('M').mean()

    # Configurar el tamaño de la figura
    fig = plt.figure(figsize=(10, 6))

    # Crear la gráfica de líneas con los datos filtrados y muestreados
    plt.plot(df_resampled.index, df_resampled['avg_temperature'], marker='o', linestyle='-', color='b')

    # Configurar los ejes y las etiquetas
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura Promedio')

    # Ajustar la rotación de las etiquetas del eje x
    plt.xticks(rotation=45)

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Mostrar el DataFrame filtrado
    st.dataframe(df_resampled)
