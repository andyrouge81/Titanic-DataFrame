#---LIBRERÍAS EMPLEADAS---#
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import streamlit as st
import plotly as pt
from streamlit_folium import st_folium
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import requests
import json


#---Nombre y configuración---#

# Nombre e icono de la web
st.set_page_config(page_title="Titanic Enhanced",
        layout="wide",
        page_icon=":ship:")

#---Eliminamos la barra superior
st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """,
    unsafe_allow_html=True)


#---Estilos para el sidebar y contenido principal
st.markdown(
    f"""
    <style>
    .sidebar-content {{
        background-color: #008080 !important;
        padding: 10px !important;
        border: 1px solid #008080 !important;
        border-radius: 5px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True)

#---Sidebar para el menú principal
logos_expediciones = ('images/logotitanic.jpg')
st.sidebar.image(logos_expediciones, width=250)
st.sidebar.header('Opciones', divider='rainbow')
st.sidebar.markdown(
    """
    <style>
    .sidebar-content {
        background-color: #000033 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

##---Lectura del archivo plano---#

enhanced = pd.read_csv('tinaticpwbi.csv')
enhanced.drop(['Unnamed: 0'], axis=1, inplace=True)

#---Opciones Menú---#
menu = st.sidebar.radio("Selecciona una opción:", ["Inicio", "Filtros", "EDA", "Power Bi","Modelo","Conclusión"]) # Cinco pilares de la App

#---Inicio---#
if menu =="Inicio":
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 60px; margin: 0; text-shadow: 6px 6px 6px #000000;'>El Titanic: </h1></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Contexto y catastrofe</h1></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
    """
    <div style="padding: 20px; color: #ffffff; font-size: 28px;">
    La madrugada del 15 de  abril de 1912 el RMS Titanic naufragó tras chocar contra un iceberg en aguas de Terranova. Tras zarpar de
    Southampton, embarcó más pasajeros en los puertos de Cherburgo (Francia) y Queenstown, actual Cohb (Irlanda). Dotado de gran lujo y comodidad
    ya que entre sus pasajeros se encontraban desde personalidades más ricas de la época hasta inmigrantes irlandeses, británicos y escandinavas que iban en busca mejores opciones en Norteamérica.
    El barco estaba dotado con las mejores medidas de seguridad de la época, sin embargo sus medidas fueron insuficientes ya que solo soportaba salvavidas para un tercio de la capacidad total del navio.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
    """
    <div style="padding: 20px; color: #ffffff; font-size: 28px;">
    En la catastrofe la cantidad de fallecidos fue mucho mayor en hombres que en mujeres y niños, a causa del proceso de evacuación "mujeres y niños primero".
    El barco se partió en dos y se hundió con cientos de personas a bordo, la mayoría de las personas que quedaron flotando, muerieron de hipotermia y los pocos botes salvavidas fueron recogidos por el RMS Carpathia horas mas tarde.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 40px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Finalidad del proyecto</h1></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        """
        <div style="padding: 20px; color: #ffffff; font-size: 28px;">
        Al tener solamente un fragmento de los datos compartidos de dicha catastrofe y puesto que ya sabemos que no hubo suficientes botes salvavidas y todo courrió muy rápido, 
        vamos a intentar comprender quien fue la pobación más catigada en el hundimiento del Titanic.
        """, unsafe_allow_html=True)
    
#---DataSet---#
if menu == "Filtros":
    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 70px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Filtros Dataset​ </h1></div>", unsafe_allow_html=True)
    
    
    
    st.sidebar.header("Filtrado pasajeros")
    
    # Creamos los filtros en el sidebar
    seleccion_super = st.sidebar.multiselect("Superviviente: ", options=enhanced["Superviviente"].unique(), default=enhanced["Superviviente"].unique())
    seleccion_sexo = st.sidebar.multiselect("Sexo: ", options=enhanced["Sexo"].unique(), default=enhanced["Sexo"].unique())
    seleccion_edad = st.sidebar.slider("Edad: ", min_value=0, max_value=90, value=(0, 90))
    seleccion_embarque = st.sidebar.multiselect("Puerta de Embarque: ", options=enhanced["Puerta_embarque"].unique(), default=enhanced["Puerta_embarque"].unique())
    seleccion_compa = st.sidebar.multiselect("Estado: ", options=enhanced["Estado"].unique(), default=enhanced["Estado"].unique())
    seleccion_precio = st.sidebar.slider("Precio Billete: ", min_value=0, max_value=550, value=(0, 550))
    
    #seleccion_estancia_mínima = st.sidebar.slider("Mínima_estancia: 🌒", min_value=1, max_value=365, value=(1, 365))

    # DataFrame con los filtros aplicados
    filtro_enhanced = enhanced.query("Superviviente == @seleccion_super & Sexo == @seleccion_sexo & Edad >= @seleccion_edad[0] & Edad <= @seleccion_edad[1] & Estado == @seleccion_compa & Puerta_embarque == @seleccion_embarque & Precio_pasaje >= @seleccion_precio[0] & Precio_pasaje <= @seleccion_precio[1]")
    st.dataframe(filtro_enhanced)

    # Resultados obtenidos
    resultado_df = filtro_enhanced.shape[0]
    st.markdown(f"*Resultados obtenidos: **{resultado_df}** *")

    st.markdown("""<br><br>""", unsafe_allow_html=True)

    st.divider()

#---EDA---#    
if menu == "EDA":

    st.markdown("<div style='padding: 10px; border-radius: 5px;'><h1 style='text-align: center; color: #ffffff; font-size: 60px; margin: 0; text-shadow: 6px 6px 6px #000000;'>Análisis Exploratorio</h1></div>", unsafe_allow_html=True)
    
    st.divider()

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 28px;">
                En esta sección vamos a ver de manera gráfica ciertos patrones que nos van a ayudar a explicar el por qué la supervivencia en mujeres y niños fue mayor que en los varones.
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        # gráfico en forma de tarta(pie) donde vemos el porcentaje de supervivientes
        sobrevive = enhanced['Superviviente'].value_counts().index.tolist()
        fig = px.pie(enhanced[enhanced['Superviviente'].isin(sobrevive)], 'Superviviente', height=400 , title='Procentaje de supervivientes', template="plotly_dark")

        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig, width=1200, height=560)
        
        st.markdown(
                    """
                    <div style="padding: 20px; color: #ffffff; font-size: 20px;">
                    Para comenzar y de manera genérica, en este gráfico de tarta podemos observar el porcentaje de los fallecidos y los supervivientes del fragmento de datos proporcionado
                    </div>
                    """, unsafe_allow_html=True)
        
    with col2:

        #gráfico que muestra los pasajeros acompañados, ya sean de familiares directos o indirectos

        st.image('images/compania.png', caption='Relación de los pasajeros que viajaban con algún tipo de familiar', width=650)

        st.markdown(
                    """
                    <div style="padding: 20px; color: #ffffff; font-size: 20px;">
                    En esta imagen podemos comparar la gente que viajaba sola, sin ningín tipo de relación con otros pasajeros y los que viajaban acompañados, ya sea de 
                    familiares directos, como padres e hijos o familiares no directos como cónyuges o hermanos.
                    Por supuesto se puede observar la grancantidad de hombres que viajan solos, esto puede ser devído a que mucha gente viajaba en busca de nuevas
                    oportunidades en Norteamérica.
                    </div>
                    """, unsafe_allow_html=True)
        
    st.divider()

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 28px;">
                Vamos a ver dos gráficos en la que filtrando a hombres y mujeres por separado, comprobaremos cual de los dos sexos viajaba acompañado y 
                la realción directa con la supervivencia de cada género.
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    col3, col4= st.columns(2)

    with col3:    
        
        st.image('images/compania1.png', caption='Tenga en cuenta que la supervivencia es de color marrón claro', width= 650)

        
    with col4:  

        st.image('images/compania2.png', caption= 'Tenga en cuenta que los supervivientes son de color verde', width=650)  

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 20px;">
                La comparación de estas dos gráficas nos da una idea de la supervivencia de mujeres y niños, ya que podemos comprobar
                la preferencia de rescate que estos tenían al ser madres e hijos, es decir, familiares directos.
                Incluso viendo que los varones tuvieron peor suerte, hay que destacar que, los varones que viajaban solos, 
                fueron sin dida los más catigados en el naufrágio.
                </div>
                """, unsafe_allow_html=True)
        
    st.divider()

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 28px;">
                Seguimos con el análisis y buscando patrones para la explicación de la alta tasa de fallecimientos en los hombres, esta vez, 
                dividimos a los pasajeros por rangos de edad, vamos a comparar la supervivencia según dichos rangos de edad.
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()

    col5, col6 = st.columns(2)

    with col5:

        st.image('images/rangofemenino.png', caption='Se aprecia la supervivencia de color rojo', width=650)

    with col6:
        
        st.image('images/rangomasculino.png', caption='Se aprecia la supervivencia de color azul', width= 650)


    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 20px;">
                Se ha dividido, según el fragmento de datos proporcionado, a los pasajeros por tres rangos de edad, 'Menores' a los niños de entre 0 y 12 años, 
                'Adultos' de entre 13 a 50 años y 'Mayores' a los que están por encima de 50 años.
                Podemos observar que se repiten ciertos patrones relacionados con el sexo , pero también con la edad de los pasajeros pues la categoría 'Adultos' es la mas castigada 
                y dentro de esta categoría siguen siendo los varones los que sufren más fallecimientos en la catastrofe.
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 28px;">
                Para terminar nuestro análisis exploratorio vamos a comparar ciertos factores que aunque son menores, también ayudan a encontrar
                ciertas pautas a la hora de explicar las consecuencias de una mayor supervicencia de mujeres en el naufragio del Titanic.
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    col7, col8 = st.columns(2)

    with col7:
        # primero seleccionamos a todas las mujeres
        female = enhanced[enhanced['Sexo']== 'Mujer']
        #vamos a ver la supervivencia de las mujeres según la edad, clase y precio del billete
        fig = px.scatter_3d(female, x='Superviviente', y='Edad', z='Precio_pasaje',
                    color='Clase')
        st.plotly_chart(fig, width=1200, height=560)

        st.markdown(
                        """
                        <div style="padding: 24px; color: #ffffff; font-size: 15px;">
                        Gráfica representativa femenina. Observe que primera clase se representa con azúl cielo.
                        </div>
                        """, unsafe_allow_html=True)

    with col8:
        # segundo, seleccionamos a todos los hombres
        male = enhanced[enhanced['Sexo']== 'Hombre']

        #vamos a ver la supervivencia de los hombres según la edad, clase y precio del billete
        fig = px.scatter_3d(male, x='Superviviente', y='Edad', z='Precio_pasaje',
                    color='Clase')
        st.plotly_chart(fig, width=1000, height=560)

        st.markdown(
                        """
                        <div style="padding: 24px; color: #ffffff; font-size: 15px;">
                        Gráfica representa maculina. Observe que primera clase se representa con azúl oscuro.
                        </div>
                        """, unsafe_allow_html=True)


    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 20px;">
                Vamos a observar estos dos gráficos interactivos en 3D, los cuales representan, la edad, el precio del pasaje y la supervivencia,
                relacionado directamente con las clases en el Titanic.
                En el gráfico de la izquierda se puede apreciar una mayor supervivencia por parte de las mujeres que viajaban en primera clase, 
                esto se ve reflejado en el precio del billete, pues las dos variables están directamente relacionadas.
                </div>
                """, unsafe_allow_html=True)
    

    st.markdown(
                """
                <div style="padding: 24px; color: #ffffff; font-size: 20px;">
                En la gráfica de la derecha, la que representa a los varones, vemos que hay fallecidos tanto en primera como en tercera clase, esto da pie,
                a que los hombres sufrieron más fallecimientos en el naufragio sin tener en cuenta su estatus social o su riqueza. Cierto es que si viajaba en tercera clase
                hubiera tenido la mala suerte de no sobrevivir al hundimiento del Titanic.
                </div>
                """, unsafe_allow_html=True)