import streamlit as st
from modulos.config.conexion import obtener_conexion
import pandas as pd

def mostrar_compra():
    st.header("📦 Registrar compra")
    try:
        con = obtener_conexion()
        cur = con.cursor()

        with st.form("form_compra"):
            proveedor = st.text_input("Proveedor")
            producto  = st.text_input("Producto")
            cantidad  = st.number_input("Cantidad", min_value=1, step=1, value=1)
            enviar = st.form_submit_button("✅ Guardar compra")

        if enviar:
            if not proveedor.strip() or not producto.strip():
                st.warning("Proveedor y producto son obligatorios.")
            else:
                try:
                    cur.execute(
                        "INSERT INTO Compras (Proveedor, Producto, Cantidad) VALUES (%s, %s, %s)",
                        (proveedor.strip(), producto.strip(), int(cantidad))
                    )
                    con.commit()
                    st.success("Compra registrada.")
                    st.rerun()
                except Exception as e:
                    con.rollback()
                    st.error(f"Error al registrar: {e}")

        # 👇 usa tu columna real y alias a 'id' si quieres
        cur.execute("""
            SELECT Id_compras AS id, Proveedor, Producto, Cantidad
            FROM Compras
            ORDER BY Id_compras DESC
        """)
        rows = cur.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=[c[0] for c in cur.description])
            st.subheader("📜 Historial de compras")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error general: {e}")
    finally:
        try: cur.close(); con.close()
        except: pass


