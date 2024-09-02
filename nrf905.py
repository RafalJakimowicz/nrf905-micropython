import machine
import time


class NRF905:

    NRF_CHANNEL = 66

    NRF_433Mhz = 0x00
    NRF_868Mhz_915Mhz = 0x02

    NRF_NEG_10dBm = 0x00
    NRF_NEG_2dBm = 0x04
    NRF_POS_6dBm = 0x08
    NRF_POS_10dBm = 0x0C

    NRF_AUTORETRAN_ON = 0x20
    NRF_AUTORETRAN_OFF = 0x00

    NRF_RX_AWF_1_BYTE = 0x00
    NRF_RX_AWF_4_BYTE = 0x04

    NRF_RX_AWF_1_BYTE = 0x00
    NRF_RX_AWF_4_BYTE = 0x40

    NRF_RX_PW_1_BYTE = 0x01
    NRF_RX_PW_2_BYTE = 0x02
    NRF_RX_PW_4_BYTE = 0x04
    NRF_RX_PW_8_BYTE = 0x08
    NRF_RX_PW_16_BYTE = 0x10
    NRF_RX_PW_32_BYTE = 0x20

    NRF_TX_PW_1_BYTE = 0x01
    NRF_TX_PW_2_BYTE = 0x02
    NRF_TX_PW_4_BYTE = 0x04
    NRF_TX_PW_8_BYTE = 0x08
    NRF_TX_PW_16_BYTE = 0x10
    NRF_TX_PW_32_BYTE = 0x20

    NRF_RX_ADDRESS_BYTE_0 = 0xCC
    NRF_RX_ADDRESS_BYTE_1 = 0xCC
    NRF_RX_ADDRESS_BYTE_2 = 0xCC
    NRF_RX_ADDRESS_BYTE_3 = 0xCC

    NRF_UP_CLK_FREQ_4MHz - 0x00
    NRF_UP_CLK_FREQ_2MHz - 0x01
    NRF_UP_CLK_FREQ_1MHz - 0x02
    NRF_UP_CLK_FREQ_500kHz - 0x03


    def __init__ (self, spi, ce, txe, pwr, cd, am, dr):
        """
        SPI - SPI connection -> must be passed co communicate
        CE - standby -> High = TX/RX, Low = standby
        TXE - mode -> High = TX, Low = RX
        PWR - power-up -> High = on, Low = off
        CD - carrier detect -> High when signal is detected
        AM - adress match -> High when receiving a packet that has same adress as one put in device
        DR - data ready -> High when finished transmitting/High when new data recieved
        """
        self.spi = spi
        self.ce = machine.Pin(ce, machine.Pin.OUT)
        self.txe = machine.Pin(txe, machine.Pin.OUT)
        self.pwr = machine.Pin(pwr, machine.Pin.OUT)
        self.cd = machine.Pin(cd, machine.Pin.OUT)
        self.am = machine.Pin(am, machine.Pin.OUT)
        self.dr = machine.Pin(dr, machine.Pin.IN)

        self.pwr.value(1)
        self.txe.value(0)

        rf_config = [0x00, 0x42]

