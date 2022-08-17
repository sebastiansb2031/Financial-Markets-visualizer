'''
High
Low
Open 
CLose
Volume
AdjClose 
'''

from curses import window
import tkinter
from turtle import color
import  pandas as pd
import numpy as np
from tkinter import ttk
from matplotlib import pyplot as plt
from pandas_datareader import data #Funcion que permite importar desde la API de finance 
import ta #Esta libreria y sus submodulos nos calcula los indicadores técnicos a partir de un dataframe de entrada
from ta.utils import dropna
from ta.volatility import BollingerBands
from sys import argv
from tkinter import *  #Libreria en donde se montó la interfaz gráfica 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt #Librearia para importar fecha actual
import yfinance as yf #Libreria para obtener los datos de yahoo finance
#import yahoo_fin 
#from yahoo_fin.stock_info import get_data
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.colors as mcolors

'''
Introducción: Las lineas de código comentadas, algunas son de prueba o inicialmente se tomaron de otros montaje de codigo para adaptarlas al nuestro. Por ahora las correcciones que habría que hacer sería mirar
más a fondo por qué algunos intervalos de tiempo no son permitidos (para ser un problema de irregularidad en el tamaño del dataframe), eso y mostrar bien los diagrama de velas porque a pesar de que se muestran no está
representado correctamente de forma visual
'''


def Graficar_indicadores():
 #TSLA= data.DataReader('TSLA', data_source= 'yahoo', start='2022-1-1') #Ticket es TSLA, dado por yahoo finance
 # TSLA= data.DataReader(str(e3.get()), data_source= 'yahoo', start=str(e1.get()), end=str(e2.get())) #Ticket es TSLA, dado por yahoo finance
 
 TSLA= yf.download(str(e3.get()), period=str(e1.get()), interval=str(e2.get()))  #Con esta simple función descargamos los datos de yahoo finance y las tenemos en un dataframe, el cual se manipula con la librería pandas, se llama TSLA pero puede tener cualquier nombre
 #e1,e2 y e3 son las variables que toma de entrada de la interfaz gráfica, así que estas son las variables a usar cuando no se se interfaz gráfica 
 #e1:Identificador y acrónimo del mercado (ej: Bitcoin:BTC-USD indice SP500:GSPC)
 #e2:periodo de muestreo, es decir cada cuanto tomamos un dato puntual 
 #e3:tiempo total de muestreo
 
 #########################PRELIMINARES###################################################
 #print(TSLA)
 t=range(len(TSLA)) #Longitud de los datos importados de yahoo financce
 g=TSLA["High"]
 #gg=TSLA.iloc[:, 0]
 print(g)

 # Load datas, aqúí solo cambiamos el nombre del dataframe que importamos con la función yf.download, a partir de aquí se usa solo el nombre de esta variable
 df = TSLA

 ###########################################################################################

 # add all available TA indicators
 ta_all_indicators_df = ta.add_all_ta_features(df, open="Open", high="High", 
                                              low="Low", close="Close", 
                                              volume="Volume")

 #Imprimir indicadores
 print(ta_all_indicators_df.iloc[:, 25]) #Importante: Dado que al importar los datos de yahoo finance tenemos un dataframe de multiples columnas, usamos la función iloc para filtrar filas y columnas, por lo que los indicadores se calcularon por ahora solo con la columna 

 #Estamos imprimiendo aquí toda la lista de los indicadores que nos muestra la consola, para elegir cual podemos usar 
 for col in ta_all_indicators_df.columns: 
     print(col)


 plt.style.use('seaborn-paper') #Fijamos el estilo o tema visual de las gráficas, este es particularmente porque ajusta la escala de las gráficas. Si usaramos otro tema tendríamos que ajustar los vectores y la escala
 ###############################################3INTERFAZ_GRAFICA###############################################################################https://datatofish.com/matplotlib-charts-tkinter-gui/

 window=Tk()#Creamos una nueva instancia de ventana, esta es la nueva ventana que nos muestra las 4 gráficas una vez que ya ingresamos el mercado y las escalas de tiempo con e1..e3.get()
 window.title('Plotting in Tkinter')#Titulo de la ventana
 window.geometry("500x500") #Fijamos el tamaño de la venta
 #Graficacion de todos los indicadores
 fig = plt.Figure(figsize=(6,5), dpi=100)#plt.Figure crea una nueva instancia de figura, es como una ventana pero en matplotlib (la librería que usamos para graficar )
 fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2) #Aquí referenciamos una figura con 4 gráficas (a1..a4) y especificamos que esté en formato de 2 filas y 2 columnas con plt.subplots(2,2)
 fig.suptitle(e3.get())
 #Fijamos el tamaño de la figura de matplotlib, el cual se debe tener cuidado que ajuste bien con el tamaño de la instancia de ventana window=TK()
 fig.set_figheight(13)
 fig.set_figwidth(10)
 ###############################################side=tkinter.CENTER
 line2 = FigureCanvasTkAgg(fig, window)
 line2.get_tk_widget().pack( fill=tkinter.BOTH)
 ###############################################################En esta sección se crean las gráficas, que en este caso se hicieron con la lista de indicadores técnicos. Se tomaron 4 particulares 
 ax1.set_title('Bandas de Bollinger')#cada gráfica tiene su propio titulo
 ax1.plot(ta_all_indicators_df["volatility_bbm"], 'tab:blue', label='Media movil') #El parámetro tab:color establece el color de la función graficada
 ax1.plot(ta_all_indicators_df["volatility_bbl"],'tab:orange', label='Banda inferior')
 ax1.plot(ta_all_indicators_df["volatility_bbh"], color='firebrick',label='Banda superior') #El color también se puede ajustar con el parámetro color, es otra manera que permite matplotlib
 ax1.set_title('Bandas de Bollinger')
 ax1.plot(g, 'tab:green')
 ax1.legend() #La linea leyend nos muestra la leyenda, el nombre de la variable y color asociado a una gráfica 
 ax1.grid(True)#Esta función nos habilita la cuadricula en la gráfica 
 ax2.plot(g,'tab:purple')
 ax2.set_title('Diagramas de velas japonesas')
 ax2.grid(True)
 ax3.plot(ta_all_indicators_df["momentum_rsi"],'tab:red')
 ax3.set_title('Indicador RSI')
 ax3.grid(True)
 ax4.plot(ta_all_indicators_df["Volume"], 'tab:blue')
 ax4.set_title('Indicador de volumen')
 ax4.grid(True)
 #window.mainloop()
 #plt.show()
 ###############################VELAS_JAPONESAS_https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/

########Entrada_usuario_TKINTER######https://python-course.eu/tkinter/entry-widgets-in-tkinter.php

Simbolos_cotizacion = {'Indices' : '^GSPC', 'Acciones' : 'TSLA', 'Criptomonedas': ['BTC-USD','ETH-USD','BNB-USD'] } #Se usa la estructura de datos de diccionarios y se imprimer en la primera ventana para que el usuario vea una pequeña lista de los indicadores 
 #Create an Entry widget to accept User Input
window2=Tk() #Creamos una nueva instancia de ventana, esta es la primera ventana que muestra al correr el programa
window2.geometry("500x500")#Tamaño de la nueva ventana que muestra las gráficas
tkinter.Label(window2, 
         text="Tiempo total de muestreo").grid(row=0)
tkinter.Label(window2, 
         text="Periodo de muestreo").grid(row=1)
tkinter.Label(window2, 
         text="Nombre").grid(row=2)


#Creamos las nuevas entradas de datos para los parámetros usados en la librería de yahoo finance (e1:Id del mercado e2:periodo muestreo e3:tiempo total de muestreo) 
e1 = tkinter.Entry(window2)
e2 = tkinter.Entry(window2)
e3 = tkinter.Entry(window2)

#posicionamos las entradas de datos con el formato de filas y columnas
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)


#La función tkinter.Button crea un botón, que cuando se presiona llama la función que uno quiera en el parámetro "command". Se ajusta su posición con los argumentos row y column (como coordenadas cartesianas)
tkinter.Button(window2, 
          text='Salir', 
          command=window2.quit).grid(row=4, 
                                    column=0, 
                                    sticky=tkinter.W, 
                                    pady=4)
#Llamamos a la función que construye todas las gráficas, la función "Graficar_indicadores"                                    
tkinter.Button(window2, 
          text='Graficar', command=Graficar_indicadores).grid(row=4, 
                                                       column=1, 
                                                       sticky=tkinter.W, 
                                                       pady=4)


#Estas son las etiquetas creadas que se ven en la primera gráfica al correr el programa, se ajusta su posición con los argumentos row y column (como coordenadas cartesianas)
tkinter.Label(window2, 
         text="Indices").grid(row=5, column=0)
tkinter.Label(window2, 
         text="Acciones").grid(row=6, column=0)
tkinter.Label(window2, 
         text="Criptomonedas").grid(row=7, column=0) 
tkinter.Label(window2, 
         text="Intervalos").grid(row=8, column=0)          
tkinter.Label(window2, 
         text=Simbolos_cotizacion['Indices']).grid(row=5, column=1)
tkinter.Label(window2, 
         text=Simbolos_cotizacion['Acciones']).grid(row=6, column=1)
tkinter.Label(window2, 
         text=Simbolos_cotizacion['Criptomonedas']).grid(row=7, column=1)
tkinter.Label(window2, 
         text="1m 2m 5m 15m 30m 90m 1h 1d 5d 1wk 1mo 3mo").grid(row=8, column=1)                                                      
window2.mainloop() #la corremos indefinidamente
