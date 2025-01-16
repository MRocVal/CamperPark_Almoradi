#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:05:01 2025

@author: manuelrocamoravalenti
"""

import streamlit as st
import pandas as pd
import os

# Configuración inicial de la app
st.set_page_config(page_title="Camper Park Almoradí", layout="wide")

# Nombre del archivo CSV
CSV_FILE = "camper_park_data.csv"

# Cargar datos desde el archivo CSV al iniciar
if "data" not in st.session_state:
    if os.path.exists(CSV_FILE):
        st.session_state["data"] = pd.read_csv(CSV_FILE)
    else:
        st.session_state["data"] = pd.DataFrame(
            columns=["Nº de plaza", "Nombre", "Día de llegada", "Día de salida estimado", "Nacionalidad", "Servicios"]
        )

# Guardar datos en el archivo CSV
def save_data_to_csv():
    st.session_state["data"].to_csv(CSV_FILE, index=False)

# Menú de navegación
menu = ["Consulta", "Búsqueda", "Modificación", "Eliminación"]
choice = st.sidebar.selectbox("Seleccione una página", menu)

# Página de Consulta
if choice == "Consulta":
    st.title("Consulta del Estado del Parking")
    if st.session_state["data"].empty:
        st.warning("No hay datos disponibles. Comienza añadiendo nuevas plazas.")
    else:
        st.dataframe(st.session_state["data"])

# Página de Búsqueda
elif choice == "Búsqueda":
    st.title("Búsqueda de Plazas")
    search_name = st.text_input("Introduce el nombre del cliente:")
    if st.button("Buscar"):
        results = st.session_state["data"][st.session_state["data"]["Nombre"].str.contains(search_name, case=False, na=False)]
        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("No se encontraron resultados para la búsqueda.")

# Página de Modificación
elif choice == "Modificación":
    st.title("Añadir o Modificar Información de Plazas")
    
    # Variables del formulario inicializadas con valores predeterminados
    plaza = st.number_input("Número de plaza:", min_value=1, value=1)
    nombre = st.text_input("Nombre:")
    llegada = st.date_input("Día de llegada:")
    salida = st.date_input("Día de salida estimado:")
    nacionalidad = st.text_input("Nacionalidad:")
    servicios = st.text_input("Servicios contratados:")

    if st.button("Guardar"):
        # Crear o actualizar el registro
        row = {
            "Nº de plaza": plaza,
            "Nombre": nombre,
            "Día de llegada": llegada,
            "Día de salida estimado": salida,
            "Nacionalidad": nacionalidad,
            "Servicios": servicios,
        }
        # Verifica si ya existe la plaza
        existing_index = st.session_state["data"][
            st.session_state["data"]["Nº de plaza"] == plaza
        ].index
        if not existing_index.empty:
            st.session_state["data"].loc[existing_index, :] = pd.DataFrame([row])
            st.success(f"Plaza {plaza} actualizada.")
        else:
            st.session_state["data"] = pd.concat(
                [st.session_state["data"], pd.DataFrame([row])], ignore_index=True
            )
            st.success(f"Plaza {plaza} añadida.")
        save_data_to_csv()

# Página de Eliminación
elif choice == "Eliminación":
    st.title("Eliminar Registros")
    delete_plaza = st.number_input("Número de plaza a eliminar:", min_value=1, value=1, key="delete_plaza")
    if st.button("Eliminar"):
        if delete_plaza in st.session_state["data"]["Nº de plaza"].values:
            st.session_state["data"] = st.session_state["data"][
                st.session_state["data"]["Nº de plaza"] != delete_plaza
            ]
            st.success(f"Registro de la plaza {delete_plaza} eliminado exitosamente.")
            save_data_to_csv()
        else:
            st.warning("El número de plaza no existe.")