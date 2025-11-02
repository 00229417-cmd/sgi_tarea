# app.py
import streamlit as st

st.set_page_config(page_title="SGI - Sistema", layout="wide")

# --- Estado de sesión por defecto ---
st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)

# --- Si NO hay sesión: mostrar login y detener ---
if not st.session_state["session_iniciada"]:
    # Import perezoso para que no falle si aún no existe el archivo
    from modulos.login import login
    login()
    st.stop()

# --- Sidebar (ya logueado) ---
with st.sidebar:
    st.header("Menú 📋")
    opcion = st.selectbox(
        "Selecciona una opción",
        ["Ventas", "Compras", "Clientes", "Otra opción"]
    )
    st.divider()
    st.caption(f"Conectado: {st.session_state['usuario']}")
    if st.button("Cerrar sesión 🔒", use_container_width=True):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.rerun()

# --- Router (imports perezosos) ---
if opcion == "Ventas":
    from modulos.venta import mostrar_venta
    mostrar_venta()

elif opcion == "Compras":
    from modulos.compra import mostrar_compra
    mostrar_compra()

elif opcion == "Clientes":
    from modulos.clientes import mostrar_clientes
    mostrar_clientes()

else:
    st.title("⚙️ Otras funciones")
    st.info("Aquí puedes agregar reportes u otras secciones.")
    from modulos.config.conexion import obtener_conexion
import streamlit as st

try:
    con = obtener_conexion()
    st.success("✅ Conectado correctamente a Clever Cloud MySQL")
    con.close()
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")


