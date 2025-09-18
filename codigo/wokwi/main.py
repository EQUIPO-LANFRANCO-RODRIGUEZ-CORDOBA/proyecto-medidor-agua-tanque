print("Hello, ESP32-S3!")

from machine import Pin
import utime
from machine import time_pulse_us   #time_pulse_us se usa para medir cuanto tiempo en micro segundos un pin permanece en alto o bajo
from machine import I2C
import network                      

from umqtt.simple import MQTTClient #Para trabajar con MQTT

from lcd_api import LcdApi


from machine_i2c_lcd import I2cLcd

# Conexión WiFi
ssid = "Wokwi-GUEST"         
password = "" 

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Conectando a WiFi...")
while not wifi.isconnected():
    utime.sleep(1)
print("Conectado! IP:", wifi.ifconfig()[0])


# Conectarse a un servidor MQTT:
# Configuración del broker
MQTT_BROKER = "test.mosquitto.org"      # Direccion de mi broken
CLIENT_ID = "ESP32_Nivel"               # Id de mi cliente
TOPIC_SUB = b"tanque/luz"               # Topico al que me suscribo para leer valores
TOPIC_PUB = b"tanque/nivel"             # Topico al que publico el valor del nivel

# Conectar al broker

client = MQTTClient(
    CLIENT_ID,                 # ID único de tu ESP32
    MQTT_BROKER,               # Dirección del broker (IP o dominio)
    port=1883,                 # Puerto MQTT (1883 sin SSL, 8883 con SSL)
)


client.connect()

print("Conectado al broker MQTT")

# Callback: qué hacer cuando llega un mensaje

def mensaje_llegado(topic, msg):            # topic y msg son variables cuyos valores son asignados por la libreria simple.mqtt al recibir un mensaje en un topico
    print("Mensaje en:", topic, "=>", msg)
    if msg.decode() == "prender":                 # Comparo el mensaje recibido convertido a texto
        led_verde.value(1)                  # Enciendo el led verde
    elif msg.decode() == "apagar":               # Comparo el mensaje recibido convertido a texto
        led_verde.value(0)                  # Apago el led verde


########################

client.set_callback(mensaje_llegado)        # Al llegar un mensaje a un topico suscripto, ejecuto la funcion "mensaje_llegando"



# Suscribirse a un tema
client.subscribe(TOPIC_SUB)
print("Suscrito a:", TOPIC_SUB)


# nota de la instalacion fisica del sensor:
print("\nNOTA: Se considera que el sensor esta ubicado a 400 cm por encima del fondo del tanque, y el mismo se usa para medir la distancia que hay entre el sensor y el pelo de agua en el tanque\n")
utime.sleep(5)
#

I2C_BUS=I2C(0, scl=Pin(35), sda=Pin(36), freq=400000)  # Inicio el bus I2C (Nº 0) en los pines 35 y 36
devices = I2C_BUS.scan()                               # Escaneo direccion de los dispositivos IC2 conectados al BUS
print("Direccion de dispositivos I2C:",devices)

led_rojo = Pin(40,Pin.OUT)
disparo = Pin(5,Pin.OUT)
eco=Pin(6,Pin.IN)
led_verde = Pin(20,Pin.OUT)         # Empleo el PIN GPIO20 como salida para conectar el led verde

#funcion para medir distancia

def medir():
    #disparo.value(0)           # pongo el pin de disparo en 0
    #time.sleep_us(5)          # espero 5 micro segundos
    disparo.value(1)           # pongo el ping de disparo en 1 (alto)     
    utime.sleep_us(10)         # espero 10 micro segundos con el ping de disparo en alto, que es el tiempo de disparo o ancho de pulso minomo recomendado por los datos del sensor
    disparo.value(0)           # pongo la salida de disparo del sensor de distancia en cero nuevamente en bajo

    tiempo_eco=time_pulse_us(eco,1,23200)    # mido el tiempo en que la entrada eco permanece en alto, el cual me va a determinar la distancia medida por el sensor. Espera en la medicion hasta los 23200 que corresponden a la maxima distancia que mide el sensor (400 cm ) 400*58=23200
    
    distancia_cm=(tiempo_eco)/58
    return distancia_cm


# Inicializar LCD 16x2
lcd = I2cLcd(I2C_BUS, 0x27, 2, 16)

while True:
    
    nivel=400 - medir()

    print("\nEl nivel de agua medido en el tanque es de: ",nivel," cm")

    #Alarma por nivel bajo
    if nivel < 100:
        led_rojo.value(1)    # Enciendo el led rojo de alerta de nivel bajo si el nivel es inferior a los 100 cm
        print("PRECAUCION! Nivel bajo ! Nivel por debajo de los 100 cm")
    else:
        led_rojo.value(0)    # Apago el led si el nivel esta por enciam de los 100 cm
        
    lcd.clear()
    lcd.putstr("Nivel medido:")
    lcd.move_to(0,1)
    lcd.putstr(str(nivel)+" cm")


# Comunicacion con el broken:

    #client.check_msg()  # Revisa si hay mensajes nuevos
    # Ejemplo: publicar cada 5 segundos
    client.publish(TOPIC_PUB, str(nivel))
    print("Valor de nivel enviado al broken:", nivel," cm")
    
    client.check_msg()    # Reviso si hay un menssaje nuevo en algun topico. Si hay se ejecutara el callback, si no hay continuo el codigo

    utime.sleep(5)       # espero 10 segundo antes de repetir el ciclo


