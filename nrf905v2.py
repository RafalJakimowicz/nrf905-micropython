import machine
import utime

class NRF905:
    NRF_WC_COMMAND = 0x00
    NRF_RC_COMMAND = 0x10
    NRF_WTP_COMMAND = 0x20
    NRF_RTP_COMMAND = 0x21
    NRF_WTA_COMMAND = 0x22
    NRF_RTA_COMMAND = 0x23
    NRF_RRP_COMMAND = 0x24


    def __init__ (self, sck, mosi, miso, ce, txe, pwr, cd, am, dr, cs):
        """
        SCK - system clock 
        MOSI - system in
        MISO - system out
        CE - standby -> High = TX/RX, Low = standby
        TXE - mode -> High = TX, Low = RX
        PWR - power-up -> High = on, Low = off
        CD - carrier detect -> High when signal is detected
        AM - adress match -> High when receiving a packet that has same adress as one put in device
        DR - data ready -> High when finished transmitting/High when new data recieved
        CS - chip select -> Used to write command to spi
        """
        self.mosi = mosi
        self.miso = miso
        self.sck = sck
        self.ce = machine.Pin(ce, machine.Pin.OUT, value=0)
        self.txe = machine.Pin(txe, machine.Pin.OUT, value=0)
        self.pwr = machine.Pin(pwr, machine.Pin.OUT, value=1)
        self.cd = machine.Pin(cd, machine.Pin.IN)
        self.am = machine.Pin(am, machine.Pin.IN)
        self.dr = machine.Pin(dr, machine.Pin.IN)
        self.cs = machine.Pin(cs, machine.Pin.OUT, value=1)
        self.spi = machine.SPI(0, baudrate=100000, mosi=self.mosi, miso=self.miso, sck=self.sck)

        self.config_bytes = [0x76, 0x0E, 0x44, 0x20, 0x20, 0xCC, 0xCC, 0xCC, 0xCC, 0x58]
        self.address_bytes = [0xCC, 0xCC, 0xCC, 0xCC]

    def writeConfig(self):
        self.cs.value(0)
        self.spi.write(self.NRF_WC_COMMAND)
        self.spi.write(self.config_bytes)
        self.cs.value(1)

    def readConfig(self):
        buff = [0x00] * 10
        self.cs.value(0)
        self.spi.write(self.NRF_RC_COMMAND)
        buff = self.spi.read(10, 0x00)
        self.cs.value(1)

    def rxPacket(self):
        buff = [0x00] * 32
        self.ce.value(0)
        self.cs.value(0)
        utime.sleep_ms(1)
        self.spi.write(bytearray(self.NRF_RRP_COMMAND))
        utime.sleep_ms(1)
        buff = self.spi.read(32, 0x00)
        self.cs.value(1)
        utime.sleep_ms(1)
        self.ce.value(1)
        utime.sleep_ms(1)
        return buff

    def txPacket(self, _packet):
        self.cs.value(0)
        self.spi.write(bytearray(self.NRF_WTP_COMMAND))
        self.spi.write(bytearray(_packet))
        self.cs.value(1)
        utime.sleep_ms(1)
        self.cs.value(0)
        self.spi.write(bytearray(self.NRF_WTA_COMMAND))
        self.spi.write(bytearray(self.address_bytes))
        self.cs.value(1)
        self.ce.value(1)
        utime.sleep_ms(1)
        self.ce.value(0)

    def setRx(self):
        self.txe.value(0)
        self.ce.value(1)
        utime.sleep_ms(1)

    def setTx(self):
        self.txe.value(1)
        self.ce.value(1)
        utime.sleep_ms(1)

    def tx(self, _packet):
        self.setTx()
        utime.sleep_ms(1)
        self.txPacket(_packet=_packet)
        
    def rx(self):
        self.setRx()
        utime.sleep_ms(1)
        data = self.rxPacket()
        return data

