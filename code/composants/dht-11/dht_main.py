from machine import Pin
import utime

from dht import DHT11, InvalidChecksum

# défini la broche pour les données et tire la broche vers le bas pour lire les données
pin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

#attend une seconde pour laisser le capteur s'allumer
utime.sleep(1)

while True:

    # pour obtenir le temps
    (year, month, day, hour, minute, second, millis, _tzinfo) = utime.localtime()
    
    # on imprime la date et le temps
    print("Date: %d-%02d-%02d Time: %02d:%02d:%02d" % (year, month, day, hour, minute, second))
    
    try:
        print("Temperature: {}".format(sensor.temperature))
        print("Humidty: {}".format(sensor.humidity))
    #except InvalidChecksum:
    except:
        print("Checksum from the sensor was invalid")
    
    print("\n")
    # temps entre la lecture des données
    utime.sleep(1)