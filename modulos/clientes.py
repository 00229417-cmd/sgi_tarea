# modulos/clientes.py
import streamlit as st
from modulos.config.conexion import obtener_conexion
import pandas as pd

def mostrar_clientes():
    st.header("👥 Registro y listado de clientes")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # --- FORMULARIO PARA AGREGAR CLIENTES ---
        with st.expander("➕ Agregar nuevo cliente", expanded=True):
            with st.form("form_cliente"):
                nombre = st.text_input("Nombre completo")
                email = st.text_input("Correo electrónico")
                telefono = st.text_input("Teléfono")
                enviar = st.form_submit_button("✅ Guardar cliente")

                if enviar:
                    if nombre.strip() == "":
                        st.warning("⚠️ El campo 'Nombre' es obligatorio.")
                    else:
                        try:
                            cursor.execute(
                                "INSERT INTO Clientes (Nombre, Email, Telefono) VALUES (%s, %s, %s)",
                                (nombre, email, telefono)
                            )
                            con.commit()
                            st.success(f"✅ Cliente registrado: {nombre}")
                            st.rerun()
                        except Exception as e:
                            con.rollback()
                            st.error(f"❌ Error al registrar cliente: {e}")

        # --- LISTADO DE CLIENTES ---
        try:
            cursor.execute("SELECT Id_clientes, Nombre, Email, Telefono FROM Clientes ORDER BY Id_clientes DESC")
            filas = cursor.fetchall()
            if filas:
                df = pd.DataFrame(filas, columns=["ID", "Nombre", "Email", "Teléfono"])
                st.subheader("📋 Lista de clientes")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Aún no hay clientes registrados.")
        except Exception as e:
            st.error(f"Error al cargar los clientes: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
