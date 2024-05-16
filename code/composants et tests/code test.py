import machine
import utime

# Définir les broches GPIO connectées à chaque segment de l'afficheur 7 segments
segments = [machine.Pin(x, machine.Pin.OUT) for x in [16,17,18,19,15,14,13,12]]

# Définir les configurations pour afficher chaque chiffre (0 à 9)
digit_patterns = [
    [1, 1, 1, 1, 1, 1, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0, 0, 1],  # 3
    [0, 1, 1, 0, 0, 1, 1],  # 4
    [1, 0, 1, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1],  # 6
    [1, 1, 1, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 0, 0, 1, 1]   # 9
]

def display_digit(digit):
    pattern = digit_patterns[digit]
    for pin, state in zip(segments, pattern):
        pin.value(state)

# Exemple d'utilisation pour afficher le chiffre 5
display_digit(3)
