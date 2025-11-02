import streamlit as st
import mysql.connector

def obtener_conexion():
    # Configura tus credenciales en st.secrets["db"]
    # [db] host="", user="", password="", database=""
    cfg = st.secrets["db"]
    return mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        autocommit=True,
    )

