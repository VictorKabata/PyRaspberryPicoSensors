import time

import machine

pin_led = machine.Pin("LED", machine.Pin.OUT)
sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / 65535


def main():
    try:
        record_temp = float(input("What temperature do you want to monitor? "))
    except ValueError:
        raise ValueError("Invalid temperature input")

    while True:
        temperature = get_temp()

        led_controller(state=(temperature >= record_temp))

        temperature_record = {"timestamp": get_timestamp(time.localtime()), "temperature": temperature}

        print(f"Temperature record: {temperature_record}")


# Get temperature of the surrounding from sensor
def get_temp():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    time.sleep(1)

    return temperature


# Toggles LED on/off depending on state passed
def led_controller(state):
    if state:
        pin_led.on()
    else:
        pin_led.off()


def get_timestamp(timestamp):
    return f"{timestamp[0]}-{timestamp[1]}-{timestamp[2]}T{timestamp[3]}:{timestamp[4]}:{timestamp[5]}Z"


if __name__ == "__main__":
    main()
