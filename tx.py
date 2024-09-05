import nrf905v2
import utime

radio = nrf905v2.NRF905(18, 19, 16, 27, 28, 26, 22, 20, 21, 18)

while True:
    x = [0x00] * 32
    for a in range(32):
        x[a] = 0x69
    radio.tx(x)
