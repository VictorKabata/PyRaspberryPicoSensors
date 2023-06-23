# Basic script to toggle LED based on threshold temp set and save records to a CSV file

import time

import machine

pin_led = machine.Pin("LED", machine.Pin.OUT)
sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / 65535


def main():
    # Get user input for the threshold temp
    try:
        record_temp = float(input("What temperature do you want to monitor? "))
    except ValueError:
        raise ValueError("Invalid temperature input!")

    while True:
        # Get current temperature from sensor
        temperature = get_temp()

        # Toggle LED if current temperature exceed threshold temp
        led_controller(state=(temperature >= record_temp))

        temperature_record = {
            "timestamp": get_timestamp(time.localtime()),
            "temperature": temperature,
        }

        # Print temperature record to the terminal
        print(f"Temperature record: {temperature_record}")

        # Record temperature record into csv file if temp exceed threshold temp
        if temperature >= record_temp:
            record_temperature(record=temperature_record)


# Get temperature of the surrounding from sensor
def get_temp(timer=1):
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    time.sleep(timer)

    return temperature


# Toggles LED on/off depending on state passed
def led_controller(state):
    if state:
        pin_led.on()
    else:
        pin_led.off()


# Get current date time as timestamp in UTC format
def get_timestamp(timestamp):
    return f"{timestamp[0]}-{timestamp[1]}-{timestamp[2]}T{timestamp[3]}:{timestamp[4]}:{timestamp[5]}Z"


# Save threshold temperature records into a CSV file
def record_temperature(record):
    with open("temperature.csv", "a") as file:
        if len(file.readlines()) == 0:
            file.write("timestamp, temperature\n")
            file.write(f"{record['timestamp']}, {record['temperature']}\n")
        else:
            file.write(f"{record['timestamp']}, {record['temperature']}\n")


if __name__ == "__main__":
    main()
