import streamlit as st
from modulos.config.conexion import obtener_conexion
import pandas as pd

def mostrar_clientes():
    st.header("👥 Clientes")

    try:
        con = obtener_conexion()
        cur = con.cursor()

        # Alta
        with st.expander("➕ Nuevo cliente", expanded=True):
            with st.form("form_cliente"):
                nombre = st.text_input("Nombre")
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")
                enviar = st.form_submit_button("✅ Guardar cliente")

            if enviar:
                if not nombre.strip():
                    st.warning("El nombre es obligatorio.")
                else:
                    try:
                        cur.execute(
                            "INSERT INTO Clientes (Nombre, Email, Telefono) VALUES (%s, %s, %s)",
                            (nombre, email, telefono)
                        )
                        con.commit()
                        st.success("Cliente guardado.")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"Error al guardar: {e}")

        # Listado
        try:
            cur.execute("SELECT Id_clientes, Nombre, Email, Telefono FROM Clientes ORDER BY Id_clientes DESC")
            rows = cur.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Nombre", "Email", "Teléfono"])
                st.subheader("📋 Lista de clientes")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Aún no hay clientes.")
        except Exception as e:
            st.error(f"Error al cargar: {e}")

    except Exception as e:
        st.error(f"Error general: {e}")
    finally:
        try: cur.close(); con.close()
        except: pass

