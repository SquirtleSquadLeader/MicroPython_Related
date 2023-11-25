from machine import I2C
from register import RORegBit, RWRegBit, RORegStruct, RORegBits, RWRegBits
import struct

class Reg:
    SECONDS = const(0x00)
    MINUTES = const(0x01)
    HOURS = const(0x02)
    DAY = const(0x03)
    DATE = const(0x04)
    MON_CENT = const(0x05)
    YEAR = const(0x06)
    A1_SEC = const(0x07)
    A1_MIN = const(0x08)
    A1_HOUR = const(0x09)
    A1_DAY_DATE = const(0x0A)
    A2_MIN = const(0x0B)
    A2_HOUR = const(0x0C)
    A2_DAY_DATE = const(0x0D)
    CTRL = const(0x0E)
    CTRL_STS = const(0x0F)
    OFFSET = const(0x10)
    TEMP_H = const(0x11)
    TEMP_L = const(0x12)
    
class SQWaveFreq:
    ONE_HZ = const(0)
    ONE_KHZ = const(1)
    FOUR_KHZ = const(2)
    EIGHT_KHZ = const(3)
    
class DS3231:
    def __init__(self, i2c, addr=0x68):
        self._i2c = i2c
        self._dev_addr = addr
        self._clock_buf = bytearray(7)
                
        self._A1IE = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 0, '>B')
        self._A2IE = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 1, '>B')
        self._INTCN = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 2, '>B')
        self._RS = RWRegBits(self._i2c, self._dev_addr, Reg.CTRL, 1, 3, 4, '>B')
        self._CONV = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 5, '>B')
        self._BBSQW = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 6, '>B')
        self._EOSC = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 7, '>B')
        
        self._A1F = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 0, '>B')
        self._A2F = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 1, '>B')
        self._BSY = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 2, '>B')
        self._EN32kHz = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 3, '>B')
        self._OSF = RWRegBit(self._i2c, self._dev_addr, Reg.CTRL, 1, 7, '>B')
        
        self._offset = RORegStruct(self._i2c, self._dev_addr, Reg.OFFSET, 1, '>b')
        self._temp = RORegStruct(self._i2c, self._dev_addr, Reg.TEMP_H, 2, '>h')
        
        print('DS3231 found at', hex(self._dev_addr))

    @property
    def temperature(self):
        return ((self._temp.__get__()>>6)*0.25)
    
    @staticmethod
    def comp_seconds(data):
        tens = ((data>>4)&7)*10
        singles = data&15
        return tens+singles
    
    @staticmethod
    def comp_minutes(data):
        tens = ((data>>4)&7)*10
        singles = data&15
        return tens+singles
    
    @staticmethod
    def comp_hours(data):
        tens = ((data>>4)&1)*10
        singles = data&15
        return tens+singles
    
    @staticmethod
    def comp_day(data):
        if data == 1:
            return 'Sunday'
        if data == 2:
            return 'Monday'
        if data == 3:
            return 'Tuesday'
        if data == 4:
            return 'Wednesday'
        if data == 5:
            return 'Thursday'
        if data == 6:
            return 'Friday'
        if data == 7:
            return 'Saturday'
        
    @staticmethod
    def comp_date(data):
        tens = ((data>>4)&3)*10
        singles = data&15
        return(tens+singles)
    
    @staticmethod
    def comp_month(data):
        tens = ((data>>4)&1)*10
        singles = data&15
        month = tens + singles
        
        if month == 1:
            return 'January'
        if month == 2:
            return 'February'
        if month == 3:
            return 'March'
        if month == 4:
            return 'April'
        if month == 5:
            return 'May'
        if month == 6:
            return 'June'
        if month == 7:
            return 'July'
        if month == 8:
            return 'August'
        if month == 9:
            return 'September'
        if month == 10:
            return 'October'
        if month == 11:
            return 'November'
        if month == 12:
            return 'December'
        
    @staticmethod
    def comp_year(data):
        tens = ((data>>4)&15)*10
        singles = data&15
        month = tens + singles
        
        
    def rtc_clock(self):
        self._i2c.readfrom_mem_into(self._dev_addr, Reg.SECONDS, self._clock_buf )
        data = struct.unpack('>bbbbbbb',self._clock_buf)         
        return f"{self.comp_year(data[6])} {self.comp_month(data[5])} {self.comp_date(data[4])} {self.comp_day(data[3])} {self.comp_hours(data[2])}:{self.comp_minutes(data[1])}:{self.comp_seconds(data[0])}"
    