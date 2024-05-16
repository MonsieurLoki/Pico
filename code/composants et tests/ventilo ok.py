from machine import Pin
import time

# Configuration de la broche GPIO 2
enable_pin = Pin(14, Pin.OUT)

# Fonction pour allumer le ventilateur
def turn_on_fan():
    enable_pin.value(1)
    print("Ventilateur allumé")

# Fonction pour éteindre le ventilateur
def turn_off_fan():
    enable_pin.value(0)
    print("Ventilateur éteint")

# Exemple d'utilisation
if __name__ == "__main__":
    while True:
        turn_on_fan()
        time.sleep(5)  # Garde le ventilateur allumé pendant 5 secondes
        turn_off_fan()
        time.sleep(5)  # Garde le ventilateur éteint pendant 5 secondes
