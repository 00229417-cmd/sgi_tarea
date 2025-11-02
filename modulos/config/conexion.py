# modulos/config/conexion.py
import os
import streamlit as st
import mysql.connector

def _cfg():
    if "db" in st.secrets:
        cfg = st.secrets["db"]
        return dict(
            host=cfg.get("host"),
            port=int(cfg.get("port", 3306)),
            user=cfg.get("user"),
            password=cfg.get("password"),
            database=cfg.get("database"),
        )
    # Fallback: variables de entorno
    return dict(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def obtener_conexion():
    cfg = _cfg()
    faltantes = [k for k,v in cfg.items() if k!="port" and (v is None or v=="")]
    if faltantes:
        raise RuntimeError(
            "Faltan credenciales de BD. Define st.secrets['db'] o variables "
            f"de entorno: {', '.join(faltantes)}"
        )
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        autocommit=True,
    )
