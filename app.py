# app.py
import streamlit as st
from modulos.login import login
from modulos.venta import mostrar_venta
from modulos.compra import mostrar_compra
from modulos.clientes import mostrar_clientes  # 👈 Nuevo módulo

# Configuración general de la página
st.set_page_config(page_title="SGI - Sistema de Gestión", layout="wide")

# --- CONTROL DE SESIÓN ---
# Si no existe la variable en la sesión, se crea con valores por defecto
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)

# --- CUERPO PRINCIPAL ---
if st.session_state["session_iniciada"]:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.header("Menú principal 📋")
        seleccion = st.selectbox(
            "Selecciona una opción",
            ["Ventas", "Compras", "Clientes", "Otra opción"]
        )
        st.divider()
        st.caption(f"Conectado como: {st.session_state['usuario']}")

        # Botón para cerrar sesión
        if st.button("Cerrar sesión 🔒", use_container_width=True):
            st.session_state["session_iniciada"] = False
            st.session_state["usuario"] = None
            st.success("Sesión cerrada correctamente.")
            st.rerun()

    # --- CONTENIDO SEGÚN LA OPCIÓN SELECCIONADA ---
    if seleccion == "Ventas":
        mostrar_venta()

    elif seleccion == "Compras":
        mostrar_compra()

    elif seleccion == "Clientes":
        mostrar_clientes()

    elif seleccion == "Otra opción":
        st.title("⚙️ Otras funciones")
        st.info("Aquí puedes agregar más secciones o reportes del sistema.")

else:
    # --- PANTALLA DE LOGIN ---
    login()
