import nrf905
import utime

radio = nrf905.NRF905(18, 19, 16, 27, 28, 26, 22, 20, 21, 17)

while True:
    x = [0x00] * 32
    for a in range(32):
        x[a] = 0x11
    radio.NRF_TX_BUFFER = x
    print(x)
    radio.TX()
    utime.sleep_ms(1750)
