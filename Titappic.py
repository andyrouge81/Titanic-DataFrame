# importamos librerias

import streamlit as st  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly as pt


# empezamos a crear nuestro streamlit con la página principal
st.set_page_config(page_title="TITANIC", page_icon=':ice_cube:' ,layout="wide") 



# cargamos la base de datos
@st.cache_resource #decorador para cachear los datos
def cargar_datos(): #función para cargar los datos
    return pd.read_csv('/Users/andresrojo/Desktop/Bootcamp/Temario/Modulo1/Proyecto_modulo1/Titanic/titanicc.csv', index_col=0) 
# se ha realizado una copia del dataframe con el que se ha estado trabajando
#llamada a nuestra funcion que carga la base de datos en formato csv
df = cargar_datos() 


# creamos un menú de barra lateral para poder poner los diferentes opciones a elegir 
opcion = st.sidebar.radio('Elige una opcion: ', ['Introducción',
                                                 'Análisis Pasajeros',
                                                 'Roles y títulos nobiliarios',
                                                 'Supervivientes por sexo',
                                                 'Supervivientes por Clase',
                                                 'Supervivientes por edades',
                                                 'Puertas de Embarque','Ver Dataframe'])



# declaramos nuestras funciones donde van a ejecutarse las diferentes opciones declaradas arriba

def mostrar_inicio():# funcion introducción

    st.header("Bienvenidos al Titanic", divider= 'rainbow')

    st.image('graficos/Titanic_Portada.jpg', use_column_width=True,caption='Fotografía de Francis Godolphin Osbourne Stuart - http://www.uwants.com/viewthread.php?tid=3817223&extra=page%3D1')
   
    st.markdown('''<span style="font-size: 28px;">Una pequeña Introducción:</span>''',unsafe_allow_html=True)

    st.markdown('''<span style="font-size: 24px;">El RMS Titanic fue un transatlántico británico que naufragó en las aguas de océano Atlántico 
                durante la noche del 14 y la madrugada del 15 de abril de 1912, mientras realizaba su viaje inaugural desde Southampton a 
                Nueva York, tras chocar con un iceberg. En el  hundimiento murieron 1496 personas de las 2208 que iban a bordo.
                En este proyecto se va  a realizar un estudio  de la base de datos del Titanic donde la importancia de variables como el sexo o la clase, 
                jugaron un papel muy importante  en el  desastre marítimo  más importante del sigloXX.</span>''',unsafe_allow_html=True)
    st.write('\n\n')
    
    
   
#funcion Análisis pasajeros
   
def calcula_edad():
    #calculamos la media de la edad agrupado por la clase

    average_age_sex = df.groupby('Clase')['Edad'].mean().reset_index()

    # ponemos unas pestañas para separar info

    tab1, tab2 = st.tabs(["Media edad por clase", "Precio del pasaje por edad"])
    
    with tab1:
        # grafico line donde vemos la media por clases
        fig=px.line(average_age_sex, x='Clase', y='Edad', title='Media de la Edad por clases del Titanic', template="plotly_dark", color_discrete_sequence=['yellow'])
        st.plotly_chart(fig, use_container_width=True)   

        st.markdown('''<span style="font-size: 24px;">Vamos a analizar un poco los pasajeros de nuestro barco. En esta gráfica vamos a representar la media de edad relacionada con el tipo de clase de los pasajeros del Titanic, 
                    siendo la primera clase la de mejor posición social. Comprobamos que los pasajeros de primera clase tienen una media de edad de 36 años, teniendo en cuenta que para la época ya eran personas asentadas, 
                    casadas y con un estatus social alto. </span>''',unsafe_allow_html=True)
    
    with tab2:
        # gráfico donde que representa los pasajeros y el precio del billete

        st.markdown('''<span style="font-size: 18px;">Precio del pasaje según las edades</span>''',unsafe_allow_html=True)
        
        fig = px.scatter(df, x="Edad", y='Precio pasaje', template="plotly_dark")
        st.plotly_chart(fig)
        
        st.markdown('''<span style="font-size: 24px;">En base a lo observado antes podemos ver una concentración de compra del pasaje entre 25 y 36 años .
                    Se puede observar ciertos pasajeros más jovenes con gran poder adquisitivo y unos condes que fueron los que mas pagaron por sus pasajes, entorno a 512 libras de la época
                    un precio que sólo muy pocos podían permitirse. </span>''',unsafe_allow_html=True)

#seguimos con el analisis de los pasajeros

#funcion que muestra los títulos y roles

def titulos():

    st.markdown('''<span style="font-size: 22px;">Estados, títulos y profesiones .</span>''',unsafe_allow_html=True)
    # generamos mas pestañas para separar info
    tab1, tab2, tab3 = st.tabs(["Clase y título"," Supervivientes", "Supervivencia por Roles"])

    with tab3:
       # en esta operación sacamos de los nombres los titulos y roles de los pasjeros
        titles=df['Titulos']= df['Nombre'].apply(lambda x: x.split(',')[1].split('.')[0])
        titles.value_counts()
       #atencion que esta es la tercera pestaña donde se muestra una relación entre lla gente que sobrevivió y los titulos y roles
        fig = px.bar(df, x='Titulos', y='Superviviente', template="plotly_white")
        st.plotly_chart(fig)

        st.markdown('''<span style="font-size: 24px;">En 1912 se clasificaba a las personas por su estado, los títulos nobiliarios y los puestos en el barco.
                   Así podemos ver que el precio de los pasajes según el estatus. Podemos eencontrar desde Mr. o Miss hasta condes,
                    maestros, doctores, por supuesto en esta primera gráfica podemos ver como los títulos van en relación con el precio del pasaje,
                    y por supuesto según la titulación o cargo el pasaje costaba mas o menos. 
                    </span>''',unsafe_allow_html=True)   
    
    
    with tab2:
        # un grafico con distintas tablas a modo de información con los supervivientes
        col1, col2, col3 = st.columns(3)
        col1.write('Porcentaje de fallecidos y supervivientes')
        col2.write('Número de personas fallecidas y supervivientes')
        col3.write('Personas fallecidas siendo uno, los supervivientes')


        col1, col2, col3 = st.columns([1,1,1]) # variables columnas
    
        with col1:
            st.image('graficos/grafico_pie.png', caption='Fig2.Gráfico tipo pie')

            
        with col2:
        # numero total de supervivientes agrupados por clase
            total=df['Superviviente'].groupby(df['Clase']).value_counts().rename('Total')
            total
        with col3: 
        # numero total de supervivientes
            total=df['Superviviente'].value_counts().rename('Total')
            total

        st.markdown('''<span style="font-size: 24px;">Una vez visto los roles y títulos por clase ya nos
                    hacemos una idea de los pasajeros que contenía el Titanic. 
                    Ahora vamos a presentar unos datos donde se muestra el porcentaje de muertes por el naufragio, 
                    los supervivientes por clase y el total de supervivientes..</span>''',unsafe_allow_html=True)
        st.write('\n\n')
 
    with tab1: 
        # grafifico que muestra las tres clases y donde se alojaban por titulos
        st.image('graficos/titulos_striplot.png', caption='Fig1.Gráfico tipo stripplot')

        st.markdown('''<span style="font-size: 24px;">En el 1912 la importancia del estatus social, la clase, los títulos nobiliarios y el estado civil tenía mucha más importancia de la que le podemos dar hoy día.
                    Podíamos encontrar de pasajeros roles como Mr. o Miss, Lady o incluso maestros, doctores o incluso condes
                     y de como dichos títulos iban en relación con el precio del pasaje,
                   así pues en primera clase viajaba la alta sociedad de la época, mientras que en segunda y tercera clase viajaban personas de un estatus social bajo. 
                    </span>''',unsafe_allow_html=True)

# empezamos el analisis por sexo 

def survivedxsex():
    # con dos pestañas, la primera muestra información
    
    st.markdown('''<span style="font-size: 22px;">Consecuencias de códigos de honor.</span>''',unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Código de honor", "Supervivientes por Sexo"])
    
    with tab1:
       col1, col2,  = st.columns([1,1])
       
       with col1:
            filtro1= df.loc[:,['Sexo','Superviviente']].value_counts().rename('Total')
            st.dataframe(filtro1)
        
            st.markdown('''<span style="font-size: 24px;">En esta tabla podemos observar rapidamente como muerieron muchos mas hombres que mujeres,
                    al grito de ¡Mujeres y niños primero!.
                   Es un código de conducta cuando los recursos de supervivencia eran limitados, en este caso, botes salvavidas.
                     En los siglos XIX y XX se consideraba un ideal caballeresco, su práctica aparecía en los relatos de algunos naufragios del siglo XVIII.
                           </span>''',unsafe_allow_html=True)
       with col2:
                st.image('graficos/mujeres.jpg', caption= 'Pintura de Thomas Hemy del HMS Birkenhead que ilustra esta práctica.')
    with tab2:
        #esta segunda muestra los supervivientes por sexo
        st.image('graficos/grafico_sex.png', caption= 'Gráfico tipo countplot')
    
        st.markdown('''<span style="font-size: 24px;">Como podemos observar en la gráfica siendo los supervivientes los de color 
                mas oscuro (1), como sobrevivieron muchas mas mujeres que hombres los cuales no tuvieron tanta 
                suerte siendo 468 hombres muertos contra 81 muertes por parte de las mujeres. </span>''',unsafe_allow_html=True)


# seguimos con analisis de supervivientes por clase y sexo

def survivex():  
    
    st.markdown('''<span style="font-size: 22px;">¿Cuántos superviviente hubo por tipo de Clase?</span>''',unsafe_allow_html=True)
   

    tab1, tab2 = st.tabs(["Relación entre Clase y sexo", "Datos consulta"])
    
    with tab1:
# mostramos grafico tipo calor 
        st.image('graficos/Heatmap_clases.png', caption= 'Fig3.Gráfico tipo Heatmap')
        
        st.markdown('''<span style="font-size: 24px;">En el siguiente gráfico lo vemos más notablemente, hemos agrupado por clases a los hombres y mujeres
                    , de mas oscuro a mas claro el indice de mortalidad, siendo negro la muerte. Podemos observar en la parte mas oscura como los hombres 
                     perdieron la vida considerablente en comparación con las mujeres, pero además, la segunda y tercera clase fueron
                     más castigadas del naufragio.</span>''',unsafe_allow_html=True)
    
# mostramos tabla con   numeros absolutos de vivos y muertos
    with tab2:
        
        clases = df.groupby(['Sexo', 'Superviviente'])['Clase'].value_counts().rename('Total')
        clases
        st.markdown('''<span style="font-size: 24px;">En esta tabla podemos observar, por ejemplo, los hombres de primera clase que murieron
                    77 en total, mientras que mujeres de primera clase solo fueron 3, de igual manera vemos que 
                    las clases mas bajas fueron las más catigadas.</span>''',unsafe_allow_html=True)

#funcion que analiza los superviventes por rangos de edad          
   
def rango():  

    st.markdown('''<span style="font-size: 22px;">¿Cuántos superviviente hubo por Rangos de edad?</span>''',unsafe_allow_html=True)

# tambien por pestañas
    tab1, tab2 = st.tabs(["Relación Edad-Supervivientes", "Datos consulta"])
#primera pestaña con la comparación de supervivientes con los tres tramos de rango de edad
    with tab1:

        st.image('graficos/rango_countplot.png', caption= 'Fig4.Gráfico tipo Heatmap')
    
        st.markdown('''<span style="font-size: 24px;">Se ha agrupado por tres rangos de edad , "Jóvenes","Adultos" y "Mayores", 
                    y así poder ver la cantidad de personas supervivientes en dichos rangos de edad. Podemos observar que el rango
                    de edad más castigado  son los adultos, mientras que aquí tenemos otro claro ejemplo de 
                    “niños y mujeres primero". .</span>''',unsafe_allow_html=True)  
    
  # mas datos de consulta con una tabla   
    with tab2:
        
        clases = df.groupby(['Rango_Edad', 'Superviviente'])['Clase'].value_counts().rename('Total')
        clases
        st.markdown('''<span style="font-size: 24px;">En la tabla podemos explorar por Rango de edad, a qué clase pertenecieron y la cantidad 
                    de Supervivientes. .</span>''',unsafe_allow_html=True)
        
 # a modo de curiosidad esta funcion relaciona las muestes con las puertas de embarque  por sexo    
          
def p_embarque():

    st.markdown('''<span style="font-size: 22px;">Supervivientes y las puertas de embarque.</span>''',unsafe_allow_html=True)
   
   #grafico ed barras que muestra la relación de los embarcados y las muertes

    fig = px.bar(df, x="Puerta de embarque", y="Superviviente", color="Sexo", title="Diferentes paradas en el  trayecto")
    st.plotly_chart(fig, theme="streamlit", caption='verde')
    
    
    st.markdown('''<span style="font-size: 24px;"> El Titanic en su trayecto tuvo diversas paradas, Southamtom, Queenstown, Cherbourg, donde recogió pasajeros, en esta gráfica podemos comprobar
                que según la puerta de embarque tales como Cherbourg y seguidamente en Queentown, tiene relación directa con la supervivencia. De esto podemos deducir que los pasajeros recogidos en Cherbourg y Queenstown 
                se establecieron en segunda y tercera clase, concluyendo que la puerta de embarque de Southamtom está relacionada con los pasajeros que embarcaron en primera clase.
                 </span>''',unsafe_allow_html=True)
    
# data frame resultante a modo de curiosidad con los datos 
def data_frame():
    st.write('DATAFRAME TITANIC')
    st.dataframe(df)
    st.text('Desliza o agranda para ver la Base de datos de los pasajeros')   
    st.markdown('''<span style="font-size: 24px;">A modo de curiosidad, en este apartado se muestra la base de datos.</span>''',unsafe_allow_html=True)

# este diccionario nos ayuda a llamar a todas las opciones de la barra lateral

opciones = { 
    "Introducción": mostrar_inicio,
    'Análisis Pasajeros' : calcula_edad,
    'Roles y títulos nobiliarios' : titulos,
    'Supervivientes por sexo' :survivedxsex,
    'Puertas de Embarque' : p_embarque,
    'Supervivientes por edades': rango,
    'Supervivientes por Clase' : survivex,
    'Ver Dataframe' : data_frame,
    
}

opciones[opcion]() #mostrar la opción seleccionada
