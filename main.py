import nrf905
import utime

radio = nrf905.NRF905(18, 16, 19, 27, 28, 26, 22, 20, 21, 18)

while True:
    radio.RX()

    print(radio.NRF_RX_BUFFER)
    radio.NRF_RX_BUFFER = [0x00] * radio.NRF_RX_BUFFER_LENGHT
