import serial

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
ser.flush()
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    c = input('Key')
    ser.write(str.encode(c))

