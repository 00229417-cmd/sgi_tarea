import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_compra():
    st.header("📦 Registrar compra simple")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Formulario para registrar la compra
        with st.form("form_compra"):
            proveedor = st.text_input("Nombre del proveedor")
            producto = st.text_input("Nombre del producto comprado")
            cantidad = st.number_input("Cantidad comprada", min_value=1, step=1)
            enviar = st.form_submit_button("✅ Guardar compra")

            if enviar:
                if proveedor.strip() == "" or producto.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del proveedor y del producto.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Compras (Proveedor, Producto, Cantidad) VALUES (%s, %s, %s)",
                            (proveedor, producto, str(cantidad))
                        )
                        con.commit()
                        st.success(f"✅ Compra registrada correctamente: {producto} (Cantidad: {cantidad}) de {proveedor}")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar la compra: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

