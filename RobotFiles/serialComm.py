import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        text = input()
        if ser.is_open:
            ser.write(text.strip().encode())
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)