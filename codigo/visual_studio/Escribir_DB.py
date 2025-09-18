# (Se requiere el modulo "mysql-connector-python" para poder conectarse a MySQL server.Pude instalarse con el comando "pip install mysql-connector-python")
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def crear_tabla_e_insertar(nivel_valor):
    try:
        # Conexión a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Caro88",
            database="esp32"
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Crear tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NIVEL (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hora DATETIME NOT NULL,
                    nivel VARCHAR(50) NOT NULL
                )
            """)

            # Insertar registro con hora actual
            dia_hora = datetime.now()
            cursor.execute(
                "INSERT INTO NIVEL (hora, nivel) VALUES (%s, %s)",
                (dia_hora, nivel_valor)
            )
            conn.commit()

            print(f"✅ Registro insertado: Nivel = {nivel_valor}, Fecha y Hora = {dia_hora}")

    except Error as e:
        print(f"❌ Error al conectar o insertar en la base de datos: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

