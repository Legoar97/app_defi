# Importaciones necesarias
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.stats import linregress
import statsmodels.api as sm

# Función para calcular el precio del bono sin cupón
def calcular_precio_bono_sin_cupon(fecha_compra, fecha_final, tasa_actual, valor_esperado, fecha_emision):
    tiempo_actual = (fecha_compra - fecha_emision).days / 365
    tiempo_vencimiento = (fecha_final - fecha_emision).days / 365
    precio = valor_esperado * np.exp(-tasa_actual * tiempo_vencimiento)
    return precio

# Función para calcular el valor presente del flujo de caja del bono
def calcular_vp(flujo_caja, tasa_porcentual_diaria, dias):
    tasa_diaria = tasa_porcentual_diaria / 100
    valor_presente = flujo_caja / ((1 + tasa_diaria) ** dias)
    return valor_presente

def bono_sin_cupon():
    st.title('Calculadora de Bonos Sin Cupón')
    fecha_emision = st.date_input('Fecha de emisión del bono:', datetime.date.today())
    fecha_final = st.date_input('Fecha de vencimiento del bono:', datetime.date.today())
    fecha_compra = st.date_input('Fecha compra:', min_value=fecha_emision, max_value=fecha_final)
    valor_esperado = st.number_input('Ingrese el valor esperado del bono:', min_value=0.0)
    tasa_emision = st.number_input('Ingrese la tasa de emisión:', format="%f") / 100
    tasa_actual = st.number_input('Ingrese la tasa actual:', format="%f") / 100

    if st.button('Calcular Precio del Bono y Evaluación de Inversión'):
        precio = calcular_precio_bono_sin_cupon(fecha_compra, fecha_final, tasa_actual, valor_esperado, fecha_emision)
        st.write(f'Valor del bono: {precio:.2f}')
        if precio >= valor_esperado:
            st.write('La inversión no es rentable')
        else:
            st.write('La inversión es rentable')

def bono_con_cupon():
    st.title('Calculadora de Bonos Con Cupón')

    # Sidebar para la entrada de parámetros
    st.sidebar.header('Parámetros del Bono')
    fecha_compra = st.sidebar.date_input('Fecha de Compra', datetime.datetime.now())
    fecha_primer_pago = st.sidebar.date_input('Fecha de Primer Pago', datetime.datetime.now())
    fecha_vencimiento = st.sidebar.date_input('Fecha de Vencimiento', datetime.date(2100, 1, 1), min_value=datetime.date(2024, 1, 1), max_value=datetime.date(2100, 12, 31))
    flujo_caja_bono = st.sidebar.number_input('Flujo de Caja del Bono', value=100.0, step=0.01)
    tasa_porcentual_diaria = st.sidebar.number_input('Tasa de Interés Diaria (en %)', value=0.05, step=0.00001, format="%.5f")
    puntos_basicos = st.sidebar.number_input('Puntos Básicos (en %)', value=0.01, step=0.00001, format="%.5f")

    # Asumir aquí más lógica de cálculo según sea necesario...

def acciones():
    st.title("Análisis de Acciones")

    ticker = st.text_input('Ingrese el símbolo de la acción:', 'AAPL')
    start_date = st.date_input('Fecha de inicio:', datetime.date.today() - datetime.timedelta(days=365))
    end_date = st.date_input('Fecha de fin:', datetime.date.today())

    if st.button('Mostrar Análisis de Acción'):
        data = yf.download(ticker, start=start_date, end=end_date)
        st.line_chart(data['Close'])

# Navegación
st.sidebar.title('Navegación')
opcion = st.sidebar.radio('Ir a:', ('Bono con Cupón', 'Bono Sin Cupón', 'Acciones'))

if opcion == 'Bono Sin Cupón':
    bono_sin_cupon()
elif opcion == 'Bono con Cupón':
    bono_con_cupon()
elif opcion == 'Acciones':
    acciones()
