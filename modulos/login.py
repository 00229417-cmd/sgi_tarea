# modulos/login.py
import streamlit as st
from modulos.config.conexion import obtener_conexion

def login():
    st.title("🔐 Iniciar sesión")

    usuario = st.text_input("Usuario")
    contra  = st.text_input("Contraseña", type="password")

    if st.button("Entrar", use_container_width=True):
        try:
            con = obtener_conexion()
            cur = con.cursor()
            # 👇 Usa los nombres reales de tu tabla Empleados
            cur.execute(
                "SELECT 1 FROM Empleados WHERE Usuario=%s AND Contra=%s LIMIT 1",
                (usuario.strip(), contra.strip())
            )
            ok = cur.fetchone() is not None
            cur.close(); con.close()
        except Exception as e:
            st.error(f"Error de conexión o consulta: {e}")
            return

        if ok:
            st.session_state["session_iniciada"] = True
            st.session_state["usuario"] = usuario
            st.success(f"¡Bienvenido, {usuario}!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


