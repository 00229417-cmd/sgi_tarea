import streamlit as st
from modulos.config.conexion import obtener_conexion
from contextlib import closing

class AuthError(Exception):
    pass

def verificar_usuario(usuario: str, contra: str):
    """
    Retorna un dict con info del usuario si las credenciales son válidas.
    Si no hay coincidencia, retorna None.
    Si falla la conexión, levanta AuthError.
    """
    try:
        con = obtener_conexion()
    except Exception as e:
        # Si tu función lanza excepción, la atrapamos aquí.
        raise AuthError(f"Error al obtener conexión: {e}")

    if not con:
        # Si retorna None o algo falsy
        raise AuthError("No se pudo conectar a la base de datos.")

    # Si llegamos aquí, hubo conexión: marcamos estado 1 sola vez
    st.session_state["conexion_exitosa"] = True

    try:
        with closing(con.cursor()) as cursor:
            # ⚠️ Ajusta la consulta a las columnas reales que necesitas.
            # Idealmente deberías tener una columna 'Tipo' o 'Rol'.
            query = """
                SELECT Usuario, Tipo
                FROM Empleados
                WHERE Usuario = %s AND Contra = %s
            """
            cursor.execute(query, (usuario, contra))
            row = cursor.fetchone()
            if not row:
                return None
            # row[0]=Usuario, row[1]=Tipo (ajusta a tu esquema real)
            return {"usuario": row[0], "tipo": row[1]}
    finally:
        con.close()

def login():
    st.title("Inicio de sesión")

    # Mensaje persistente si alguna vez se conectó correctamente
    if st.session_state.get("conexion_exitosa"):
        st.success("✅ Conexión a la base de datos establecida correctamente.")

    with st.form("login_form", clear_on_submit=False):
        usuario = st.text_input("Usuario", key="Usuario_input")
        contra = st.text_input("Contraseña", type="password", key="Contra_input")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        # Validaciones básicas
        if not usuario or not contra:
            st.warning("Ingresa usuario y contraseña.")
            return

        try:
            info = verificar_usuario(usuario, contra)
        except AuthError as e:
            # Solo error de conexión / DB aquí
            st.error(f"⚠️ {e}")
            return
        except Exception as e:
            # Cualquier otro error inesperado
            st.exception(e)
            return

        if info is None:
            # Aquí SOLO mostramos credenciales incorrectas (ya hubo conexión)
            st.error("❌ Credenciales incorrectas.")
            return

        # Éxito
        st.session_state["usuario"] = info["usuario"]
        st.session_state["tipo_usuario"] = info["tipo"]  # ahora sí es el rol
        st.session_state["sesion_iniciada"] = True
        st.success(f"Bienvenido ({info['usuario']}) 👋")
        st.rerun()
