import streamlit as st

st.set_page_config(page_title="SGI - Sistema", layout="wide")
from modulos.config.conexion import obtener_conexion
import streamlit as st

with st.expander("🧪 Probar conexión a MySQL", expanded=False):
    if st.button("Probar conexión"):
        with st.spinner("Intentando conectar..."):
            try:
                con = obtener_conexion()
                cur = con.cursor()
                cur.execute("SELECT NOW()")
                st.success(f"✅ Conectado. Hora del servidor: {cur.fetchone()[0]}")
                cur.close(); con.close()
            except Exception as e:
                st.error(f"❌ No se pudo conectar: {e}")

st.session_state.setdefault("session_iniciada", False)
st.session_state.setdefault("usuario", None)

if not st.session_state["session_iniciada"]:
    from modulos.login import login
    login()
    st.stop()

with st.sidebar:
    st.header("Menú 📋")
    opcion = st.selectbox("Selecciona una opción", ["Ventas", "Compras", "Clientes", "Otra opción"])
    st.divider()
    st.caption(f"Conectado: {st.session_state['usuario']}")
    if st.button("Cerrar sesión 🔒", use_container_width=True):
        st.session_state["session_iniciada"] = False
        st.session_state["usuario"] = None
        st.rerun()

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



