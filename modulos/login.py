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

            # Usa tu tabla real:
            # Opción A (como en tu BD): Empleados(usuario, clave)
            cur.execute(
                "SELECT 1 FROM Empleados WHERE usuario=%s AND clave=%s LIMIT 1",
                (usuario, clave)
            )

            # Opción B (si usas USUARIO con SHA2) — reemplaza la consulta de arriba:
            # cur.execute("SELECT 1 FROM USUARIO WHERE usuario=%s AND clave_hash=SHA2(%s,256) LIMIT 1",
            #             (usuario, clave))

            ok = cur.fetchone() is not None
            cur.close(); con.close()

            if ok:
                st.session_state["session_iniciada"] = True
                st.session_state["usuario"] = usuario
                st.success("¡Bienvenido!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
        except Exception as e:
            st.error(f"Error de conexión/consulta: {e}")

