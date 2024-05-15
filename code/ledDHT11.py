import dht
import machine
import utime

# Configuration des broches pour les LEDs et le capteur DHT11
pin_dht = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Broche de données du capteur DHT11 (GPIO 18)
pin_led_green = machine.Pin(19, machine.Pin.OUT)  # LED verte (GPIO 19)
pin_led_red = machine.Pin(21, machine.Pin.OUT)   # LED rouge (GPIO 21)

# Initialisation du capteur DHT11
sensor = dht.DHT11(pin_dht)

# Lecture de la température
def read_temperature():
    try:
        # Lecture des données depuis le capteur
        sensor.measure()
        # Récupération de la température
        temperature = sensor.temperature()
        return temperature
    except OSError as e:
        print("Erreur lors de la lecture du capteur DHT11:", e)
        return None

# Fonction pour contrôler les LEDs en fonction de la température
def control_leds(temperature):
    if temperature is not None:
        if temperature < 25:
            # Température en dessous de 25°C
            pin_led_green.on()
            pin_led_red.off()
        else:
            # Température de 25°C ou plus
            pin_led_green.off()
            pin_led_red.on()
    else:
        # En cas d'erreur de lecture de température, éteindre les LEDs par sécurité
        pin_led_green.off()
        pin_led_red.off()

# Exemple d'utilisation
while True:
    temperature = read_temperature()
    control_leds(temperature)
    if temperature is not None:
        print("Température: {}°C".format(temperature))
    utime.sleep(2)  # Attendre 2 secondes entre chaque lecture
