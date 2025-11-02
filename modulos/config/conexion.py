# modulos/config/conexion.py
import streamlit as st
import mysql.connector

def obtener_conexion():
    cfg = st.secrets["db"]
    return mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        port=int(cfg.get("port", 3306)),
        autocommit=True,
        connection_timeout=6
    )

