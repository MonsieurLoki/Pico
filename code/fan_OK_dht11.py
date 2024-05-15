import machine
import utime
import dht

# Configure the sensor data pin
DATA_PIN = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

# Create an instance of the DHT22 sensor
sensor = dht.DHT11(DATA_PIN)
temperature = None
humidity = None

def read_and_display_data():

    global temperature
    global humidity
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
#         print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temperature, humidity))
    except Exception as e:
        print("Error reading sensor data:", e)


def main():
    i = 1
    # Main loop
    while True:
        read_and_display_data()
        utime.sleep(1)  # Wait for 1 seconds before reading the data again
        i += 1
        print(i, "temperature:", temperature, "  humidity:", humidity)

if __name__ == "__main__":
    main()

