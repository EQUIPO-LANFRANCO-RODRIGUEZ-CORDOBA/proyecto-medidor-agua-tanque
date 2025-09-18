# requiere tener instalado la libreria "paho-mqtt",
# Se puede instalar desde la ventana de comando ejecutando el comando: "pip install paho-mqtt")
# (Se requiere el modulo "mysql-connector-python"
# para poder conectarse a MySQL server.
# Pude instalarse con el comando "pip install mysql-connector-python")
"""
Script para recibir datos de nivel de agua por MQTT y almacenarlos en MySQL.
Requiere instalar las librerías:
- paho-mqtt: pip install paho-mqtt
- mysql-connector-python: pip install mysql-connector-python
"""

import paho.mqtt.client as mqtt
from mysql.connector import Error
from Escribir_DB import crear_tabla_e_insertar

# Configuración del broker MQTT
BROKER = "test.mosquitto.org"
PUERTO = 1883
TOPIC = "tanque/nivel"

def on_connect(client, userdata, flags, rc):
    """
    Función que se ejecuta al conectar con el broker MQTT.
    """
    if rc == 0:
        print("Conectado al broker exitosamente.")
        client.subscribe(TOPIC)
        print(f"Suscripto al tópico: {TOPIC}")
    else:
        print(f"Error de conexión. Código: {rc}")

def on_message(client, userdata, msg):
    """
    Función que se ejecuta al recibir un mensaje del broker.
    Decodifica el mensaje y lo inserta en la base de datos.
    """
    try:
        nivel = msg.payload.decode()
        print(f"Mensaje recibido en {msg.topic}: {nivel}")
        crear_tabla_e_insertar(nivel)
    except Error as err:
        print(f"Error al insertar en la base de datos: {err}")
    except Exception as err:
        print(f"Error inesperado: {err}")

def main():
    """
    Función principal: configura el cliente MQTT y lo pone a escuchar.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"Conectando al broker {BROKER} en el puerto {PUERTO}...")
        client.connect(BROKER, PUERTO, 60)
        client.loop_forever()
    except Exception as err:
        print(f"Error al conectar al broker: {err}")

if __name__ == "__main__":
    main()
