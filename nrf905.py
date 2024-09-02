import machine
import time


class NRF905:
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
        self.ce = ce
        self.txe = txe
        self.pwr = pwr
        self.cd = cd
        self.am = am
        self.dr = dr