# Projet Pico Smart Fan
EPHEC, Technologies de l'Informatique, Electronique 2

Groupe J:
- Gaspard Derruine
- Maxime Malpica
- Hugo Noppe
- Dorian Kwizera


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [GitHub](#GitHub)

## Introduction

This is a group project from Ephec students in TI2, Electronics2

## Features

Project objectives :
- implement several functionalities on a Raspberry Pi Pico W
- monitor a temperature sensor and display it on a 2 digit 7-segment
    - use 2 SN74LS47N to drive the 7-segment digits
- when temperature is above MAX, activate fan until it's down below MAX-1
    - a simple 5v fan (DC motor) is used
    - a relay is used to ensure enough power can be given to the fan
    - (an extra power source is added to the Pico 5V source from the USB cable (or battery))
- a web server on the Pico allows to
    - consult that state of the system (temperature, etc)
    - manually control the fan (ON, OFF)
    - the MAX value can be updated with the web interface
- optional
    - implement an LCD 1602 display to show additional information
    - buzzer when temperature above MAX
    - vary the fan speed depending on the temperature (with PWM)
    - leds to indicate status
    - potentiometer (ADC) to adjust reference temperature
    - etc


## GitHub

https://github.com/MonsieurLoki/Pico

Le repository contient:
- les schémas et circuits du PCB
- le code
- le rapport d'avancement et le rapport final



