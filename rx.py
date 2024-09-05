import nrf905v2
import utime

radio = nrf905v2.NRF905(18, 19, 16, 27, 28, 26, 22, 20, 21, 18)

while True:
    print(radio.rx())

    utime.sleep_ms(500)
