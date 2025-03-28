import machine
import time
import struct
def read_measures(request):
    signed=True
    
    uart.write(request) 
    time.sleep(0.1)
    payload = uart.read()
    payload = payload[3:-2]
    response_quantity = int(len(payload) / 2)
    fmt = '>' + (('h' if signed else 'H') * response_quantity)
    return struct.unpack(fmt, payload)

def calculate_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc) 

uart = machine.UART(0, baudrate=9600, tx=0, rx=1)  # Change TX/RX pins if needed

request = bytearray([0x01, 0x04, 0x00, 0x00, 0x00, 0x0A])  
request += calculate_crc(request)  # Append CRC - Cyclic redundancy check



while True:
    try:
        #read all measures in one time
        all_measures = read_measures(request)
        print(all_measures)
        #split and print measues
        voltage = all_measures[0]/10.0
        print('U = ' + str(voltage) + ' V')
        current = ((all_measures[2]<<16) |  (all_measures[1]))/1000.0
        print('I = ' + str(current) + ' A')
        power = ((all_measures[4]<<16) |  (all_measures[3]))/10.0
        print('P = ' + str(power) + 'W')
        energy = ((all_measures[6]<<16) |  (all_measures[5]))/1000.0
        print('E = ' + str(energy) + 'kWh')
        freq = all_measures[7]/10.0
        print('freq = ' + str(freq) + ' Hz')
        pf = all_measures[8]/10.0
        print('power factor = ' + str(pf))
    except:
        print('pzem04 reading error')
    time.sleep(2)

