import dht
import machine
import utime

# Configuration des broches pour les LEDs et le capteur DHT11
pin_dht = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Broche de données du capteur DHT11 (GPIO 18)
pin_led_green = machine.Pin(19, machine.Pin.OUT)  # LED verte (GPIO 19)
pin_led_red = machine.Pin(21, machine.Pin.OUT)   # LED rouge (GPIO 21)

# Configuration des broches pour les décodeurs 74LS47
decoder_1_A = machine.Pin(9, machine.Pin.OUT)  # Bit d'entrée A du premier décodeur (GPIO 9)
decoder_1_B = machine.Pin(8, machine.Pin.OUT)  # Bit d'entrée B du premier décodeur (GPIO 8)
decoder_1_C = machine.Pin(7, machine.Pin.OUT)  # Bit d'entrée C du premier décodeur (GPIO 7)
decoder_1_D = machine.Pin(6, machine.Pin.OUT)  # Bit d'entrée D du premier décodeur (GPIO 6)

decoder_2_A = machine.Pin(5, machine.Pin.OUT)  # Bit d'entrée A du  deuxième décodeur (GPIO 5)
decoder_2_B = machine.Pin(4, machine.Pin.OUT)  # Bit d'entrée B du deuxième décodeur (GPIO 4)
decoder_2_C = machine.Pin(3, machine.Pin.OUT)  # Bit d'entrée C du deuxième décodeur (GPIO 3)
decoder_2_D = machine.Pin(2, machine.Pin.OUT)  # Bit d'entrée D du deuxième décodeur (GPIO 2)

# Initialisation des décodeurs 74LS47
def set_decoder_inputs(decoder, value):
    decoder[0].value(value & 0b0001)
    decoder[1].value(value & 0b0010)
    decoder[2].value(value & 0b0100)
    decoder[3].value(value & 0b1000)

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

# Fonction pour afficher un nombre sur les deux afficheurs à sept segments
def display_number(number):
    # Affichage des dizaines
    set_decoder_inputs([decoder_1_A, decoder_1_B, decoder_1_C, decoder_1_D], number // 10)
    # Affichage des unités
    set_decoder_inputs([decoder_2_A, decoder_2_B, decoder_2_C, decoder_2_D], number % 10)

# Exemple d'utilisation
while True:
    temperature = read_temperature()
    control_leds(temperature)
    if temperature is not None:
        print("Température: {}°C".format(temperature))
        display_number(temperature)  # Afficher la température
    utime.sleep(2)  # Attendre 2 secondes entre chaque lecture
