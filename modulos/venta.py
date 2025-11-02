import streamlit as st
from modulos.config.conexion import obtener_conexion
import pandas as pd

def mostrar_venta():
    st.header("🛒 Registrar venta")
    try:
        con = obtener_conexion()
        cur = con.cursor()

        with st.form("form_venta"):
            producto = st.text_input("Producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)
            enviar = st.form_submit_button("✅ Guardar venta")

        if enviar:
            if not producto.strip():
                st.warning("Ingresa el nombre del producto.")
            else:
                try:
                    cur.execute(
                        "INSERT INTO Ventas (Producto, Cantidad) VALUES (%s, %s)",
                        (producto.strip(), int(cantidad))
                    )
                    con.commit()
                    st.success("Venta registrada.")
                    st.rerun()
                except Exception as e:
                    con.rollback()
                    st.error(f"Error al registrar: {e}")

        # 👇 usa tu columna real y, si quieres, aliaséala a 'id'
        cur.execute("""
            SELECT Id_venta AS id, Producto, Cantidad
            FROM Ventas
            ORDER BY Id_venta DESC
        """)
        rows = cur.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=[c[0] for c in cur.description])
            st.subheader("📜 Historial de ventas")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error general: {e}")
    finally:
        try: cur.close(); con.close()
        except: pass
