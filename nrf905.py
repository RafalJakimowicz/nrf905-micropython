import machine
import utime


class NRF905:
    NRF_CHANNEL = 106 #0-511

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

    #this is default address for rx and tx
    NRF_RX_ADDRESS_BYTE_0 = 0xE7
    NRF_RX_ADDRESS_BYTE_1 = 0xE7
    NRF_RX_ADDRESS_BYTE_2 = 0xE7
    NRF_RX_ADDRESS_BYTE_3 = 0xE7

    NRF_TX_ADDRESS_0 = 0xE7
    NRF_TX_ADDRESS_1 = 0xE7
    NRF_TX_ADDRESS_2 = 0xE7
    NRF_TX_ADDRESS_3 = 0xE7

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

    NRF_RF_CONFIG_BUFFER_LENGHT = 10

    NRF_WC_COMMAND = 0x00
    NRF_RC_COMMAND = 0x10
    NRF_WTP_COMMAND = 0x20
    NRF_RTP_COMMAND = 0x21
    NRF_WTA_COMMAND = 0x22
    NRF_RTA_COMMAND = 0x23
    NRF_RRP_COMMAND = 0x24

    NRF_TX_BUFFER = [0x00] * NRF_TX_BUFFER_LENGHT
    NRF_RX_BUFFER = [0x00] * NRF_RX_BUFFER_LENGHT

    #TODO ZROB CALE SPI RECZNIE "C:\Users\Ja\Downloads\1614790577_nrf905_transceiv_other_other\NRF905_Demo\TX\Libraries\NRF905.c"
    #"C:\Users\Ja\Downloads\1614790577_nrf905_transceiv_other_other\NRF905_Demo\TX\Libraries\NRF905.h"
    #

    def __init__ (self, sck, tx, rx, ce, txe, pwr, cd, am, dr, cs):
        """
        SCK - system clock -> SPI clock
        RX - system in -> SPI receiver
        TX - system out -> SPI tranceiver
        CE - standby -> High = TX/RX, Low = standby
        TXE - mode -> High = TX, Low = RX
        PWR - power-up -> High = on, Low = off
        CD - carrier detect -> High when signal is detected
        AM - adress match -> High when receiving a packet that has same adress as one put in device
        DR - data ready -> High when finished transmitting/High when new data recieved
        CS - chip select -> SPI chip select used for writing commands to module
        """
        #innit pins
        self.tx = machine.Pin(tx, machine.Pin.OUT)
        self.rx = machine.Pin(rx, machine.Pin.IN)
        self.sck = machine.Pin(sck, machine.Pin.OUT)
        self.ce = machine.Pin(ce, machine.Pin.OUT)
        self.txe = machine.Pin(txe, machine.Pin.OUT)
        self.pwr = machine.Pin(pwr, machine.Pin.OUT)
        self.cd = machine.Pin(cd, machine.Pin.IN)
        self.am = machine.Pin(am, machine.Pin.IN)
        self.dr = machine.Pin(dr, machine.Pin.IN)
        self.cs = machine.Pin(cs, machine.Pin.OUT)

        self.pwr.value(1)
        self.txe.value(0)
        self.ce.value(0)
        self.sck.value(0)
        self.cs.value(1)

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
        BYTE_9 = (self.NRF_CRC_MODE_16_BIT + self.NRF_CRC_EN_YES + self.NRF_XOF_16Hz + self.NRF_CRC_EN_NO + self.NRF_UP_CLK_FREQ_500kHz)

        config_bytes = [self.NRF_WC_COMMAND, BYTE_0, BYTE_1, BYTE_2, BYTE_3, BYTE_4, BYTE_5, BYTE_6, BYTE_7, BYTE_8, BYTE_9]

        #writing config bytes to module
        self.cs.value(0)
        print(config_bytes)
        for _ in config_bytes:
            self._write(_)
        
        self.cs.value(1)

    def _write(self, data):
        """
        writes single byte do module
        """
        s = 0x08 #counter for bits (one byte)
        while s > 0:
            if (data & 0x80) != 0:
                self.tx.value(1)
            else:
                self.tx.value(0)

            self.sck.value(1)
            
            data <<= 0x01

            self.sck.value(0)

            s -= 1

    def _read(self):
        """
        reading byte from module
        """
        s = 0x08 #bits counter (one byte)
        data = 0x00 #byte stored

        while s > 0:
            data <<= 1

            self.sck.value(1)

            if self.rx.value():
                data |= 0x01

            self.sck.value(0)

            s -= 1

        return data


    def _set_tx_mode(self):
        self.txe.value(1) #setting module as transceiver
        self.ce.value(1) #waking from standby mode
        utime.sleep_ms(40)

    def _set_rx_mode(self):
        self.txe.value(0) #setting module as receiver
        self.ce.value(1) #waking from standby mode
        utime.sleep_ms(40)

    def _check_DR(self):
        if(self.dr.value() != 0): #check if whole packet arrive
            return 0x01
        else:
            return 0x00

    def _tx_packet(self):
        """
        send tranceiver packet to passed adress
        """
        #setting adress
        TX_ADDRESS = [0x00] * self.NRF_TX_ADDRESS_LENGHT
        TX_ADDRESS = [self.NRF_TX_ADDRESS_0, self.NRF_TX_ADDRESS_1, self.NRF_TX_ADDRESS_2, self.NRF_TX_ADDRESS_3]

        self.cs.value(0)
        self._write(self.NRF_WTP_COMMAND)
        
        #writing packet via SPI
        for _ in bytearray(self.NRF_TX_BUFFER):
            self._write(_)

        self.cs.value(1)
        utime.sleep_ms(1)

        self.cs.value(0)

        self._write(self.NRF_WTA_COMMAND)

        #writing adress for packet to arrive
        for _ in TX_ADDRESS:
            self._write(_)

        self.cs.value(1)
        self.ce.value(1)
        utime.sleep_ms(40)
        self.ce.value(0)

    def _rx_packet(self) -> None:
        """
        receiving packet from module
        """
        utime.sleep_ms(10)

        self.ce.value(0)
        self.cs.value(0)

        utime.sleep_ms(1)

        self._write(self.NRF_RRP_COMMAND)

        #reading packet to buffer
        for _ in range(self.NRF_RX_BUFFER_LENGHT):
            self.NRF_RX_BUFFER[_] = self._read()

        self.cs.value(1)
        utime.sleep_ms(40)
        self.ce.value(1)

    def TX(self):
        self._set_tx_mode() #setting in tranceiver mode
        self._tx_packet() #sending packet

    def RX(self):
        self._set_rx_mode() #setting to receiver mode
        #not comment to wait for whole packet arrive
        while(self._check_DR() == 0x00): pass
        utime.sleep_ms(40)
        self._rx_packet() #getting packet
        utime.sleep_ms(40)


