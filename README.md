# Medidor de Nivel de Agua con ESP32-S3 y Escalamiento a Capa de Transporte

 # Descripción del proyecto

Este proyecto implementa un sistema de monitoreo de nivel de agua en un tanque utilizando un microcontrolador ESP32-S3 y un sensor ultrasónico HC-SR04.

El sistema se diseñó inicialmente en la capa física (sensores y actuadores) y fue escalado hasta la capa de transporte de datos y almacenamiento, integrando comunicación mediante MQTT y persistencia en MySQL.

# Características principales:

. Medición de nivel de agua en tiempo real.

 .Alerta visual mediante LED rojo cuando el nivel es bajo (< 100 cm).

. Control remoto de un LED verde a través de mensajes MQTT.

. Comunicación WiFi simulada en Wokwi.

. Almacenamiento histórico de mediciones en MySQL mediante un backend en Python.

# Tecnologías utilizadas

Hardware simulado: ESP32-S3, sensor HC-SR04, LCD 16x2 (I2C), LEDs.

Simulación: Wokwi
.

Comunicación: MQTT (broker público test.mosquitto.org).

Lenguajes: MicroPython (ESP32-S3) y Python (backend).

Base de datos: MySQL.

Entorno de desarrollo: Visual Studio Code.

# Arquitectura del sistema
flowchart TD
    A[ESP32-S3 + Sensor HC-SR04] -->|MQTT: tanque/nivel| B[Broker MQTT test.mosquitto.org]
    B --> C[Script Python en VS Code]
    C --> D[Base de datos MySQL]
    B -->|Comandos: tanque/luz| A
    A --> E[LCD 16x2 + LEDs]

# Instalación y ejecución
1. Simulación en Wokwi

Clonar este repositorio.

Abrir el proyecto en Wokwi
.

Cargar el código del ESP32-S3 en MicroPython.

2. Configuración del backend en Python

Instalar dependencias:

pip install paho-mqtt mysql-connector-python


Ejecutar el script:

python backend.py

3. Base de datos MySQL

Crear la base de datos y la tabla:

CREATE DATABASE nivel_tanque;
USE nivel_tanque;

CREATE TABLE mediciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel FLOAT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

 # Resultados esperados

El LCD muestra el nivel del agua en tiempo real.

El LED rojo se enciende cuando el nivel < 100 cm.

El LED verde se enciende o apaga al recibir comandos por MQTT (prender / apagar).

Los datos se almacenan en MySQL con fecha y hora.

# Demostración

Video explicativo: https://youtu.be/6RuRBddahZE?si=L1kfPL6qKr4-YRkj

Informe técnico completo: [Informe técnico PDF](./documentacion/InformeTecnico.pdf)

# Equipo de desarrollo

Rodríguez Matías

Rodríguez Facundo

Córdoba Diego

Lanfranco Carolina

Lanfranco Julia

 # Futuras mejoras

Control automático de bomba según nivel.

Notificaciones móviles (Telegram/WhatsApp/Email).

Panel web para visualización y control remoto.

Integración con múltiples sensores en paralelo.
