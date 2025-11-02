import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='bzx585zwhabtxac70iyo-mysql.services.clever-cloud.com',
            user='uedi7iosseatjqpr',
            password='uedi7iosseatjqpr',
            database='bzx585zwhabtxac70iyo',
            port=3306
        )
        if conexion.is_connected():
            print("✅ Conexión establecida")
            return conexion
        else:
            print("❌ Conexión fallida (is_connected = False)")
            return None
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar: {e}")
        return None
