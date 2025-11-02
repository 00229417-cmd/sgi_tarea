import streamlit as st
from modulos.config.conexion import obtener_conexion

def login():
    st.title("Iniciar sesión")

    usuario = st.text_input("Usuario")
    clave   = st.text_input("Contraseña", type="password")

    if st.button("Entrar", use_container_width=True):
        try:
            con = obtener_conexion()
            cur = con.cursor()
            # Tu tabla y columnas reales:
            cur.execute(
                "SELECT 1 FROM Empleados WHERE usuario=%s AND clave=%s LIMIT 1",
                (usuario.strip(), clave.strip())
            )
            ok = cur.fetchone() is not None
            cur.close(); con.close()
        except Exception as e:
            st.error(f"Error de conexión o consulta: {e}")
            return

        if ok:
            st.session_state["session_iniciada"] = True
            st.session_state["usuario"] = usuario
            st.success("✅ Sesión iniciada")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")


