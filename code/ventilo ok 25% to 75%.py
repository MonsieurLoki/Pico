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

# Exemple d'utilisation
if __name__ == "__main__":
    while True:
        # Régler la vitesse du ventilateur à une valeur élevée (par exemple, 75%)
        set_fan_speed(int(0.75 * 65535))
        time.sleep(10)  # Tourne vite pendant 10 secondes
        
        # Régler la vitesse du ventilateur à une valeur plus basse (par exemple, 25%)
        set_fan_speed(int(0.25 * 65535))
        time.sleep(10)  # Tourne lentement pendant 10 secondes
