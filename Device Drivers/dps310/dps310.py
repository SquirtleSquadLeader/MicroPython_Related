from register import RORegBit, RWRegBit, RORegStruct, RORegBits, RWRegBits, ROReg24Bit
from machine import I2C
from time import sleep
import struct

class ScaleFactor:
    OSR1 = const(524288)
    OSR2 = const(1572864)
    OSR4 = const(3670016)
    OSR8 = const(7864320)
    OSR16 = const(253952)
    OSR32 = const(516096)
    OSR64 = const(1040384)
    OSR128 = const(2088960)
    
class Rate:
    RATE_1 = const(0)
    RATE_2 = const(1)
    RATE_4 = const(2)
    RATE_8 = const(3)
    RATE_16 = const(4)
    RATE_32 = const(5)
    RATE_64 = const(6)
    RATE_128 = const(7)
    
class Register:
    DEV_ADR = const (0x77)
    DEV_ADR_SDO_LO = const(0x76)
    
    # Pressure Data
    PSR_B2 = const(0x00)
    PSR_B1 = const(0x01)
    PSR_B0 = const(0x02)

    # Temperature Data
    TMP_B2 = const(0x03)
    TMP_B1 = const(0x04)
    TMP_B0 = const(0x05)

    # Configurations
    PRS_CFG  = const(0x06)
    TMP_CFG  = const(0x07)
    MEAS_CFG = const(0x08)
    CFG_REG  = const(0x09)

    # Status
    INT_STS  = const(0x0A)
    FIFO_STS = const(0x0B)

    # Reset
    RESET = const(0x0C)
 
    # Product ID
    PRODUCT_ID = const(0x0D)

    # COEFFICIENT                 Bits 7 6 5 4 3 2 1 0       
    COEF_0x10 = const(0x10) # c0       [11:4]
    COEF_0x11 = const(0x11) # c0       [3:0] / [11:8]
    COEF_0x12 = const(0x12) # c1       [7:0]
    COEF_0x13 = const(0x13) # c00      [19:12]
    COEF_0x14 = const(0x14) # c00      [11:4]
    COEF_0x15 = const(0x15) # c00/c10  [3:0] / [19:16]
    COEF_0x16 = const(0x16) # c10      [15:8]
    COEF_0x17 = const(0x17) # c10      [7:0]
    COEF_0x18 = const(0x18) # c01      [15:8]
    COEF_0x19 = const(0x19) # c01      [7:0]
    COEF_0x1A = const(0x1A) # c11      [15:8]
    COEF_0x1B = const(0x1B) # c11      [7:0]
    COEF_0x1C = const(0x1C) # c20      [15:8]
    COEF_0x1D = const(0x1D) # c20      [7:0]
    COEF_0x1E = const(0x1E) # c21      [15:8]
    COEF_0x1F = const(0x1F) # c21      [7:0]
    COEF_0x20 = const(0x20) # c30      [15:8]
    COEF_0x21 = const(0x21) # c30      [7:0]
 
    # Coefficient Source
    COEF_SRCE = const(0x28)

class DPS310:    
    def __init__(self, i2c_conn, dev_addr=Register.DEV_ADR):
        self._i2c = i2c_conn
        self._dev_addr = dev_addr
        self._readings=0
        self._pressure = 0
        self._temperature = 0
        self._kt = 0
        self._kp = 0
        self._c0 = 0
        self._c1 = 0
        self._c00 = 0
        self._c10 = 0
        self._c11 = 0
        self._c01 = 0
        self._c20 = 0
        self._c21 = 0
        self._c30 = 0     
        
        self._pm_prc = RWRegBits(self._i2c, self._dev_addr, Register.PRS_CFG, 1, 0, 3, '>B')
        self._pm_rate = RWRegBits(self._i2c, self._dev_addr, Register.PRS_CFG, 1, 4, 6, '>B')
        self._tm_prc = RWRegBits(self._i2c, self._dev_addr, Register.TMP_CFG, 1, 0, 3, '>B')
        self._tmp_rate = RWRegBits(self._i2c, self._dev_addr, Register.TMP_CFG, 1, 4, 6, '>B')
        self._tmp_ext = RWRegBit(self._i2c, self._dev_addr, Register.TMP_CFG, 1, 7, '>B')
        self._meas_ctrl = RWRegBits(self._i2c, self._dev_addr, Register.MEAS_CFG, 1, 0, 2, '>B')
        self._prs_rdy = RORegBit(self._i2c, self._dev_addr, Register.MEAS_CFG, 1, 4, '>B')
        self._tmp_rdy = RORegBit(self._i2c, self._dev_addr, Register.MEAS_CFG, 1, 5, '>B')
        self._sensor_rdy = RORegBit(self._i2c, self._dev_addr, Register.MEAS_CFG, 1, 6, '>B')
        self._coef_rdy = RORegBit(self._i2c, self._dev_addr, Register.MEAS_CFG, 1, 7, '>B')
        self._spi_mode = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG, 1, 0, '>B')
        self._fifo_en = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG, 1, 1, '>B')
        self._prs_shift_en = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG, 1, 2, '>B')
        self._tmp_shift_en = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG, 1, 3, '>B')
        self._int_sel = RWRegBits(self._i2c, self._dev_addr, Register.CFG_REG, 1, 4, 6, '>B')
        self._int_hl = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG, 1, 7, '>B')
        self._int_prs = RORegBit(self._i2c, self._dev_addr, Register.INT_STS, 1, 0, '>B')
        self._int_tmp = RORegBit(self._i2c, self._dev_addr, Register.INT_STS, 1, 1, '>B')
        self._int_fifo_full = RORegBit(self._i2c, self._dev_addr, Register.INT_STS, 1, 2, '>B')
        self._fifo_empty = RORegBit(self._i2c, self._dev_addr, Register.FIFO_STS, 1, 0, '>B')
        self._fifo_full = RORegBit(self._i2c, self._dev_addr, Register.FIFO_STS, 1, 1, '>B')
        self._soft_rst = RWRegBits(self._i2c, self._dev_addr, Register.RESET, 1, 0, 3, '>B')
        self._fifo_flush = RWRegBit(self._i2c, self._dev_addr, Register.RESET, 1, 7, '>B')
        self._prod_id = RWRegBits(self._i2c, self._dev_addr, Register.PRODUCT_ID, 1, 0, 3, '>B')
        self._rev_id = RWRegBits(self._i2c, self._dev_addr, Register.RESET, 1, 4, 7, '>B')
        
        print('DPS310 found at', hex(Register.DEV_ADR))
        self._pm_rate.__set__(Rate.RATE_1)
        self._tmp_rate.__set__(Rate.RATE_1)
        self._pm_prc.__set__(0)
        self._tm_prc.__set__(0)
        self._meas_ctrl.__set__(7)
        
        # Wait for Sensor Ready FLAG
        while(self._sensor_rdy.__get__() == 0):
            print('DPS310 Not Ready')
            sleep(0.5)
        print('DPS310 Initialized')        

        self.set_coefficients()
        self.set_k()
    
    
    def readings(self):
        self.set_readings()
        
        # Scale readings with k coefs
        temp_scaled = self._temperature/self._kt
        pressure_scaled = (self._pressure/self._kp)
        
        pres_calc = (
            self._c00
            + pressure_scaled
            * (self._c10 + pressure_scaled * (self._c20 + pressure_scaled * self._c30))
            + temp_scaled
            * (self._c01 + pressure_scaled * (self._c11 + pressure_scaled * self._c21))
        )
        return (pres_calc/68.948, temp_scaled)
        
    def set_readings(self):
        # Read RAW data from pressure and temperature registers
        self._readings = self._i2c.readfrom_mem(self._dev_addr, Register.PSR_B2, 6)
        self._readings = struct.unpack('>BBBBBB', self._readings)        
        
        # Assemble values
        self._pressure = (self._readings[0]<<16) + (self._readings[1]<<8) + self._readings[2]
        self._temperature = (self._readings[3]<<16) + (self._readings[4]<<8) + self._readings[5]
        
        # Convert to 2's compliment
        self._pressure = self.nbit2comp(self._pressure)
        self._temperature = self.nbit2comp(self._temperature)
        
        
    def set_coefficients(self):
        # Read out coef registers and assemble values
        print('\n', '=== Setting Coefficients ===')
        # Wait for Coef Ready FLAG 
        while(self._coef_rdy.__get__() == 0):
            sleep(0.5)
            
        reg_values = self._i2c.readfrom_mem(self._dev_addr, Register.COEF_0x10, 18)
        reg_values = struct.unpack('>BBBBBBBBBBBBBBBBBB', reg_values)
        
        """
        for val in range(0, len(reg_values)):
            print(reg_values[val])
        """
            
        # Set c0
        self._c0 = (reg_values[0]<< 5) + (reg_values[1] >> 5)
        if self._c0&0x800 == 0x800:
            self._c0 = -(self._c0&0x7FF)
        else:
            self._c0 = self._c0&0x7FF
        print('c0: ', self._c0)
        
        # Set c1
        self._c1 = ((reg_values[1]&0b00001111)<<8) + reg_values[2]
        if self._c1&0x800 == 0x800:
            self._c1 = -(self._c1&0x7FF)
        else:
            self._c1 = self._c1&0x7FF
        print('c1: ', self._c1)
        
        # Set c00
        self._c00 = (reg_values[3]<<12) + (reg_values[4]<<4) + (reg_values[5]>>4)
        if self._c00&0x80000 == 0x80000:
            self._c00 = -(self._c00&0x7FFFF)
        else:
            self._c00 = self._c00&0x7FFFF
        print('c00: ', self._c00)
        
        # Set c10
        self._c10 = ((reg_values[5]&0b00001111)<<16) + (reg_values[6]<<8) + reg_values[7]
        if self._c10&0x80000 == 0x80000:
            self._c10 = -(self._c10&0x7FFFF)
        else:
            self._c10 = self._c10&0x7FFFF
        print('c10: ', self._c10)
        
        # Set c01
        self._c01 = (reg_values[8]<<8) + (reg_values[9])
        if self._c01&0x8000 == 0x8000:
            self._c01 = -(self._c01&0x7FFF)
        else:
            self._c01 = self._c01&0x7FFF
        print('c01: ', self._c01)
        
        # Set c11
        self._c11 = (reg_values[10]<<8) + (reg_values[11])
        if self._c11&0x8000 == 0x8000:
            self._c11 = -(self._c11&0x7FFF)
        else:
            self._c11 = self._c11&0x7FFF
        print('c11: ', self._c11)
        
        # Set c20
        self._c20 = (reg_values[12]<<8) + (reg_values[13])
        if self._c20&0x8000 == 0x8000:
            self._c20 = -(self._c20&0x7FFF)
        else:
            self._c20 = self._c20&0x7FFF
        print('c20: ', self._c20)
        
        # Set c21
        self._c21 = (reg_values[14]<<8) + (reg_values[15])
        if self._c21&0x8000 == 0x8000:
            self._c21 = -(self._c21&0x7FFF)
        else:
            self._c21 = self._c21&0x7FFF
        print('c21: ', self._c21)
        
        # Set c30
        self._c30 = (reg_values[16]<<8) + (reg_values[17])
        if self._c30&0x8000 == 0x8000:
            self._c30 = -(self._c30&0x7FFF)
        else:
            self._c30 = self._c30&0x7FFF
        print('c30: ', self._c30)
        print('=== DPS310 Coefficients Set ===\n')
        
    def set_k(self):
        # Set kp & kt
        print('\n=== Setting kt / kp ===')
        osr_p = self._pm_prc.__get__()
        osr_t = self._tm_prc.__get__()
         
        print('OSR P T: ',osr_p, osr_t)
        
        # Pressure precision and bit shift
        if osr_p == 0b0000:
            self._kp = ScaleFactor.OSR1
            self._prs_shift_en = 0
        elif osr_p == 0b0001:
            self._kp = ScaleFactor.OSR2
            self._prs_shift_en = 0
        elif osr_p == 0b0010:
            self._kp = ScaleFactor.OSR4
            self._prs_shift_en = 0
        elif osr_p == 0b0011:
            self._kp = ScaleFactor.OSR8
            self._prs_shift_en = 0
        elif osr_p == 0b0100:
            self._kp = ScaleFactor.OSR16
            self._prs_shift_en = 1
        elif osr_p == 0b0101:
            self._kp = ScaleFactor.OSR32
            self._prs_shift_en = 1
        elif osr_p == 0b0110:
            self._kp = ScaleFactor.OSR64
            self._prs_shift_en = 1
        elif osr_p == 0b0111:
            self._kp = ScaleFactor.OSR128
            self._prs_shift_en = 1
            
        # Temperature precision and bit shift
        if osr_t == 0b0000:
            self._kt = ScaleFactor.OSR1
            self._tmp_shift_en = 0
        elif osr_t == 0b0001:
            self._t = ScaleFactor.OSR2
            self._tmp_shift_en = 0
        elif osr_t == 0b0010:
            self._kt = ScaleFactor.OSR4
            self._tmp_shift_en = 0
        elif osr_t == 0b0011:
            self._kt = ScaleFactor.OSR8
            self._tmp_shift_en = 0
        elif osr_t == 0b0100:
            self._kt = ScaleFactor.OSR16
            self._tmp_shift_en = 1
        elif osr_t == 0b0101:
            self._kt = ScaleFactor.OSR32
            self._tmp_shift_en = 1
        elif osr_t == 0b0110:
            self._kt = ScaleFactor.OSR64
            self._tmp_shift_en = 1
        elif osr_t == 0b0111:
            self._kt = ScaleFactor.OSR128
            self._tmp_shift_en = 1
        
        print('kp:', self._kp)
        print('kt:', self._kt)
        print('===  kp / kt Set ===\n')
    
    """
    @staticmethod
    def nbit2comp(value, nbits):
        sign = value&(0b1 << (nbits-1))
        mask = 0b0
        
        # Fill bit mask
        for val in range(0, (nbits-1)):
            mask = (mask<<1)+1
        
        # Generate signed integer
        if sign>0:
            return (value&mask) * -1
        else:
            return value&mask
    """
    @staticmethod
    def nbit2comp(val) -> int:
        if val&0x800000 == 0x800000:
            return -(val&0x7FFFFF)
        else:
            return val&0x7FFFFF
        
        
        
        
        
        