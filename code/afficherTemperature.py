import dht
import machine
import utime

# Configuration des broches pour les LEDs, le capteur DHT11 et les décodeurs 74LS47
pin_dht = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Broche de données du capteur DHT11 (GPIO 18)
pin_led_green = machine.Pin(19, machine.Pin.OUT)  # LED verte (GPIO 19)
pin_led_red = machine.Pin(21, machine.Pin.OUT)   # LED rouge (GPIO 21)

# Broches pour le premier décodeur (affichage des dizaines)
pin_decoder_d0 = machine.Pin(6, machine.Pin.OUT)  # Bit d'entrée D
pin_decoder_d1 = machine.Pin(7, machine.Pin.OUT)  # Bit d'entrée C
pin_decoder_d2 = machine.Pin(8, machine.Pin.OUT)  # Bit d'entrée B
pin_decoder_d3 = machine.Pin(9, machine.Pin.OUT)  # Bit d'entrée A

# Broches pour le deuxième décodeur (affichage des unités)
pin_decoder2_d0 = machine.Pin(2, machine.Pin.OUT)  # Bit d'entrée D
pin_decoder2_d1 = machine.Pin(3, machine.Pin.OUT)  # Bit d'entrée C
pin_decoder2_d2 = machine.Pin(4, machine.Pin.OUT)  # Bit d'entrée B
pin_decoder2_d3 = machine.Pin(5, machine.Pin.OUT)  # Bit d'entrée A

# Initialisation du capteur DHT11
sensor = dht.DHT11(pin_dht)

# Tableau de correspondance des segments pour l'affichage à sept segments
segments = {
    '0': 0b00111111,
    '1': 0b00000110,
    '2': 0b01011011,
    '3': 0b01001111,
    '4': 0b01100110,
    '5': 0b01101101,
    '6': 0b01111101,
    '7': 0b00000111,
    '8': 0b01111111,
    '9': 0b01101111
}

# Fonction pour afficher un chiffre sur l'affichage à sept segments
def display_digit(decoder, digit):
    pin_decoder_d0.value((segments[digit] >> 0) & 1)
    pin_decoder_d1.value((segments[digit] >> 1) & 1)
    pin_decoder_d2.value((segments[digit] >> 2) & 1)
    pin_decoder_d3.value((segments[digit] >> 3) & 1)
    pin_decoder2_d0.value((segments[digit] >> 0) & 1)
    pin_decoder2_d1.value((segments[digit] >> 1) & 1)
    pin_decoder2_d2.value((segments[digit] >> 2) & 1)
    pin_decoder2_d3.value((segments[digit] >> 3) & 1)
    decoder.value(0)

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
        # Affichage des dizaines et des unités de température sur les deux affichages
        display_digit(pin_decoder_d0, str(temperature // 10))  # Affichage des dizaines
        utime.sleep(0.005)  # Attendre un court instant pour éviter les interférences
        display_digit(pin_decoder2_d0, str(temperature % 10))  # Affichage des unités
    utime.sleep(2)  # Attendre 2 secondes entre chaque lecture
