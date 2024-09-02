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

    NRF_RX_PWR_NORMAL = 0x00
    NRF_RX_PWR_REDUCED = 0x10

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

    NRF_TX_ADDRESS_0 = 0xCC
    NRF_TX_ADDRESS_1 = 0xCC
    NRF_TX_ADDRESS_2 = 0xCC
    NRF_TX_ADDRESS_3 = 0xCC

    NRF_UP_CLK_FREQ_4MHz = 0x00
    NRF_UP_CLK_FREQ_2MHz = 0x01
    NRF_UP_CLK_FREQ_1MHz = 0x02
    NRF_UP_CLK_FREQ_500kHz = 0x03

    NRF_XOF_4MHz = 0x00
    NRF_XOF_8MHz = 0x08
    NRF_XOF_12MHz = 0x10
    NRF_XOF_16Hz = 0x18
    NRF_XOF_20MHz = 0x20

    NRF_CRC_EN_NO = 0x00
    NRF_CRC_EN_YES = 0x40

    NRF_CRC_MODE_8_BIT = 0x00
    NRF_CRC_MODE_16_BIT = 0x80

    NRF_TX_BUFFER_LENGHT = 32
    NRF_RX_BUFFER_LENGHT = 32

    NRF_TX_ADDRESS_LENGHT = 4

    NRF_RF_CONFIG_BUFFER_LENGHT = 11

    NRF_WC_COMMAND = 0x00
    NRF_RC_COMMAND = 0x10
    NRF_WTP_COMMAND = 0x20
    NRF_RTP_COMMAND = 0x21
    NRF_WTA_COMMAND = 0x22
    NRF_RTA_COMMAND = 0x23
    NRF_RRP_COMMAND = 0x24

    NRF_TX_BUFFER = [0x00] * NRF_TX_BUFFER_LENGHT
    NRF_RX_BUFFER = [0x00] * NRF_RX_BUFFER_LENGHT



    def __init__ (self, spi, ce, txe, pwr, cd, am, dr, cs):
        """
        SPI - SPI connection -> must be passed co communicate
        CE - standby -> High = TX/RX, Low = standby
        TXE - mode -> High = TX, Low = RX
        PWR - power-up -> High = on, Low = off
        CD - carrier detect -> High when signal is detected
        AM - adress match -> High when receiving a packet that has same adress as one put in device
        DR - data ready -> High when finished transmitting/High when new data recieved
        CS - chip select -> Used to write command to spi
        """
        self.spi = spi
        self.ce = machine.Pin(ce, machine.Pin.OUT)
        self.txe = machine.Pin(txe, machine.Pin.OUT)
        self.pwr = machine.Pin(pwr, machine.Pin.OUT)
        self.cd = machine.Pin(cd, machine.Pin.OUT)
        self.am = machine.Pin(am, machine.Pin.OUT)
        self.dr = machine.Pin(dr, machine.Pin.IN)
        self.cs = machine.Pin(cs, machine.Pin.OUT, value=1)

        self.pwr.value(1)
        self.txe.value(0)

        #config bytes
        BYTE_0 = (self.NRF_CHANNEL & 0x00FF)
        BYTE_1 = (self.NRF_AUTORETRAN_ON + self.NRF_RX_PWR_NORMAL + self.NRF_POS_10dBm + self.NRF_433Mhz + ((self.NRF_CHANNEL & 0x0100) >> 8))
        BYTE_2 = (self.NRF_TX_PW_4_BYTE + self.NRF_RX_AWF_4_BYTE)
        BYTE_3 = (self.NRF_RX_PW_32_BYTE & 0x3F)
        BYTE_4 = (self.NRF_TX_PW_32_BYTE & 0x3F)
        BYTE_5 = (self.NRF_RX_ADDRESS_BYTE_0)
        BYTE_6 = (self.NRF_RX_ADDRESS_BYTE_1)
        BYTE_7 = (self.NRF_RX_ADDRESS_BYTE_2)
        BYTE_8 = (self.NRF_RX_ADDRESS_BYTE_3)
        BYTE_9 = (self.NRF_CRC_MODE_16_BIT + self.NRF_CRC_EN_YES + self.NRF_XOF_16Hz + self.NRF_CRC_EN_NO + self.NRF_UP_CLK_FREQ_4MHz)

        config_bytes = [self.NRF_WC_COMMAND, BYTE_0, BYTE_1, BYTE_2, BYTE_3, BYTE_4, BYTE_5, BYTE_6, BYTE_7, BYTE_8, BYTE_9]

        #writing config value via spi to module
        try:
            cs.value(0)
            spi.write(config_bytes)
        finally:
            cs.value(1)

    def read

