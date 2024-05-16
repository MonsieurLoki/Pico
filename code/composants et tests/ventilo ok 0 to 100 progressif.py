from machine import Pin, PWM
import time

# Configuration de la broche GPIO 2 pour PWM
enable_pin = Pin(2, Pin.OUT)
pwm = PWM(enable_pin)

# Définir la fréquence PWM (par exemple, 1 kHz)
pwm.freq(1000)

# Fonction pour régler la vitesse du ventilateur
def set_fan_speed(duty_cycle):
    pwm.duty_u16(duty_cycle)
    print(f"Vitesse du ventilateur réglée à {duty_cycle / 65535 * 100:.2f}%")

# Fonction pour augmenter progressivement la vitesse du ventilateur
def ramp_up_fan_speed(duration, steps):
    for step in range(steps + 1):
        duty_cycle = int((step / steps) * 65535)
        set_fan_speed(duty_cycle)
        time.sleep(duration / steps)

# Fonction pour diminuer progressivement la vitesse du ventilateur
def ramp_down_fan_speed(duration, steps):
    for step in range(steps + 1):
        duty_cycle = int(((steps - step) / steps) * 65535)
        set_fan_speed(duty_cycle)
        time.sleep(duration / steps)

# Exemple d'utilisation
if __name__ == "__main__":
    while True:
        ramp_up_fan_speed(10, 100)  # Augmente la vitesse sur 10 secondes avec 100 paliers
        time.sleep(5)  # Maintient la vitesse maximale pendant 5 secondes
        ramp_down_fan_speed(10, 100)  # Diminue la vitesse sur 10 secondes avec 100 paliers
