import nrf905
import utime

radio = nrf905.NRF905(18, 19, 16, 27, 28, 26, 22, 20, 21, 18)

while True:
    radio.RX()
    print(radio.NRF_RX_BUFFER)

    utime.sleep_ms(500)
