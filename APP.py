#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:05:01 2025

@author: manuelrocamoravalenti
"""


import streamlit as st
import pandas as pd
import os

# Guardar datos en el archivo CSV y recargarlo
def save_data_to_csv():
    if "data" in st.session_state:
        with open("camper_park_data_modificado.csv", "w") as f:
            st.session_state["data"].to_csv(f, index=False)
        # Recargar el archivo inmediatamente después de guardar
        st.session_state["data"] = pd.read_csv("camper_park_data_modificado.csv")
        st.success("Archivo CSV guardado y recargado exitosamente como 'camper_park_data_modificado.csv'.")

# Botón para actualizar datos desde el CSV
def refresh_data():
    if os.path.exists("camper_park_data_modificado.csv"):
        st.session_state["data"] = pd.read_csv("camper_park_data_modificado.csv")
        st.success("Datos recargados desde el archivo CSV.")

# Función para descargar el archivo CSV
def download_csv():
    if "data" in st.session_state:
        csv_data = st.session_state["data"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar datos como CSV",
            data=csv_data,
            file_name="camper_park_data_modificado.csv",
            mime="text/csv"
        )





    

if choice == "Principal":
    st.title("Camper Park Almoradí")
    st.image("image1.jpeg", use_container_width=True)  # Cambia "image1.jpeg" por la ruta de tu imagen
    st.write("""
        **Bienvenidos a Camper Park Almoradí**  
        Este sistema ha sido diseñado para gestionar, coordinar y organizar el uso de las plazas en nuestro parking de una manera eficiente.  
        
        Podrás:
        - Consultar la ocupación actual.
        - Buscar clientes registrados.
        - Modificar información de las plazas.
        - Eliminar registros según necesidad.

        ¡Gracias por confiar en nosotros!
    """)

    st.button("Guardar y Recargar CSV", on_click=save_data_to_csv)
    st.button("Actualizar datos desde CSV", on_click=refresh_data)
    st.button('Hola', on_click=download_csv)
        
        
        
        
# Página de Consulta
elif choice == "Consulta":
    
    # Botón de actualizar en cada página
    if st.button("Actualizar datos"):
        refresh_data()
    # Interfaz para subir el archivo CSV
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

    # Procesar archivo subido
    if uploaded_file is not None:
        st.session_state["data"] = pd.read_csv(uploaded_file)
        # Convertir columnas de fechas al formato adecuado (si existen)
        if "Día de llegada" in st.session_state["data"]:
            st.session_state["data"]["Día de llegada"] = pd.to_datetime(st.session_state["data"]["Día de llegada"]).dt.date
        if "Día de salida estimado" in st.session_state["data"]:
            st.session_state["data"]["Día de salida estimado"] = pd.to_datetime(st.session_state["data"]["Día de salida estimado"]).dt.date
    st.title("Consulta del Estado del Parking")
    if st.session_state["data"].empty:
        st.warning("No hay datos disponibles. Comienza añadiendo nuevas plazas.")
    else:
        # Mostrar tabla de datos
        st.dataframe(st.session_state["data"])

        # Calcular el tiempo de estancia para cada plaza
        st.session_state["data"]["Duración"] = (
            pd.to_datetime(st.session_state["data"]["Día de salida estimado"]) - 
            pd.to_datetime(st.session_state["data"]["Día de llegada"])
        ).dt.days

        # Determinar el color según la duración de la estancia
        def asignar_color(duracion):
            if pd.isnull(duracion):  # Vacías
                return "blue"
            elif duracion > 10:  # Mucho tiempo
                return "red"
            elif 5 <= duracion <= 10:  # Tiempo medio
                return "yellow"
            elif duracion < 5:  # Poco tiempo
                return "green"

        st.session_state["data"]["Color"] = st.session_state["data"]["Duración"].apply(asignar_color)

        # Crear un gráfico de plazas usando Plotly
        import plotly.graph_objects as go

        fig = go.Figure()

        for index, row in st.session_state["data"].iterrows():
            fig.add_trace(go.Scatter(
                x=[row["Nº de plaza"]],
                y=[1],  # Posición ficticia para alinear las plazas
                mode="markers",
                marker=dict(size=30, color=row["Color"], symbol="square"),
                name=f"Plaza {row['Nº de plaza']} - {row['Duración']} días"
            ))

        # Configuración del gráfico
        fig.update_layout(
            title="Estado de las Plazas",
            xaxis=dict(title="Número de Plaza", tickmode="linear"),
            yaxis=dict(visible=False),  # Ocultar el eje Y
            showlegend=True,
            height=400
        )

        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)



# Página de Modificación
elif choice == "Modificación/Añadir":
    
    # Botón de actualizar en cada página
    if st.button("Actualizar datos"):
        refresh_data()
        
    st.title("Consulta del Estado del Parking")
    if st.session_state["data"].empty:
        st.warning("No hay datos disponibles. Comienza añadiendo nuevas plazas.")
    else:
        st.dataframe(st.session_state["data"])
    
    st.title("Añadir o Modificar Información de Plazas")
    
    # Selección del número de plaza
    plaza = st.number_input("Número de plaza:", min_value=1, value=1)
    
    # Buscar registro existente por número de plaza
    existing_row = st.session_state["data"][
        st.session_state["data"]["Nº de plaza"] == plaza
    ]
    
    # Inicializar campos con valores existentes si el registro ya está en la base de datos
    if not existing_row.empty:
        existing_row = existing_row.iloc[0]
        nombre = st.text_input("Nombre:", value=existing_row["Nombre"])
        llegada = st.date_input("Día de llegada:", value=pd.to_datetime(existing_row["Día de llegada"]))
        salida = st.date_input("Día de salida estimado:", value=pd.to_datetime(existing_row["Día de salida estimado"]))
        nacionalidad = st.text_input("Nacionalidad:", value=existing_row["Nacionalidad"])
        servicios = st.text_input("Servicios contratados:", value=existing_row["Servicios"])
    else:
        # Si no hay un registro existente, campos vacíos
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
    st.dataframe(st.session_state["data"])
    # Botón de actualizar en cada página
    if st.button("Actualizar datos"):
        refresh_data()
        
    st.title("Eliminar Registros")
    delete_plaza = st.number_input("Número de plaza a eliminar:", min_value=1, value=1, key="delete_plaza")
    
    # Buscar el registro correspondiente a la plaza
    registro_a_eliminar = st.session_state["data"][
        st.session_state["data"]["Nº de plaza"] == delete_plaza
    ]
    
    if not registro_a_eliminar.empty:
        # Mostrar información del cliente antes de la confirmación
        st.write("**Detalles del cliente aparcado:**")
        st.table(registro_a_eliminar)
        
        # Confirmación del usuario
        if st.button("Confirmar eliminación"):
            st.session_state["data"] = st.session_state["data"][
                st.session_state["data"]["Nº de plaza"] != delete_plaza
            ]
            st.success(f"Registro de la plaza {delete_plaza} eliminado exitosamente.")
            save_data_to_csv()
    else:
        st.warning("El número de plaza no existe.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        