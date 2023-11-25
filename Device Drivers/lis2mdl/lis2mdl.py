from machine import Pin, I2C
import struct
from register import RORegBit, RWRegBit, RORegStruct, RORegBits, RWRegBits

class Register:
    # 00 - 44 RESERVED - DO NOT USE
        
        """ Hard-iron registers """
        OFFSET_X_REG_L = const(0x45)
        OFFSET_X_REG_H = const(0x46)
        OFFSET_Y_REG_L = const(0x47)
        OFFSET_Y_REG_H = const(0x48)
        OFFSET_Z_REG_L = const(0x49)
        OFFSET_Z_REG_H = const(0x4A)
        
        # 4B - 4C RESERVED - DO NOT USE
        
        WHO_AM_I = const(0x4F)
        
        # 50 - 5F RESERVED
        
        """ Configuration Registers """
        CFG_REG_A = const(0x60)
        CFG_REG_B = const(0x61)
        CFG_REG_C = const(0x62)
        
        """ Interrupt Configuration Registers """
        INT_CTRL_REG = const(0x63)
        INT_SOURCE_REG = const(0x64)
        INT_THS_L_REG = const(0x65)
        INT_THS_H_REG = const(0x66)
        
        """ Status """
        STATUS_REG = const(0x67)
        
        """ Output Registers """
        OUTX_L_REG = const(0x68)
        OUTX_H_REG = const(0x69)
        OUTY_L_REG = const(0x6A)
        OUTY_H_REG = const(0x6B)
        OUTZ_L_REG = const(0x6C)
        OUTZ_H_REG = const(0x6D)
        
        """ Temperature Sensor Registers """
        TEMP_OUT_L_REG = const(0x6E)
        TEMP_OUT_H_REG = const(0x6F)


class LIS2MDL:
    
    def __init__(self, i2c):        
        self._i2c = i2c
        self._dev_addr = 0x1E
        
        cfga=struct.pack('<B', 0x8C)
        cfgc=struct.pack('<B', 0x10)
        self._i2c.writeto_mem(self._dev_addr, Register.CFG_REG_A, cfga)
        self._i2c.writeto_mem(self._dev_addr, Register.CFG_REG_C, cfgc)
        
        
        self._who_am_i = RORegBits(self._i2c, self._dev_addr, Register.WHO_AM_I, 1, 0, 7)
        
        self._mode = RWRegBits(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 0, 1, '<B')        
        self._odr = RWRegBits(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 2, 3, '<B')        
        self._lp = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 4, '<B')
        self._soft_rst = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 5, '<B')
        self._reboot = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 6, '<B')
        self._comp_temp_en = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_A, 1, 7, '<B')
        
        self._lpf = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_B, 1, 0, '<B')
        self._off_canc = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_B, 1, 1, '<B')
        self._set_freq = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_B, 1, 2, '<B')
        self._int_on_dataoff = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_B, 1, 3, '<B')
        self._off_canc_one_shot = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_B, 1, 4, '<B')
    
        self._drdy_on_pin = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 0, '<B')
        self._self_test = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 1, '<B')
        self._4wspi = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 2, '<B')
        self._ble = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 3, '<B')
        self._bdu = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 4, '<B')
        self._i2c_dis = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 5, '<B')
        self._int_on_pin = RWRegBit(self._i2c, self._dev_addr, Register.CFG_REG_C, 1, 6, '<B')
        
        self._ien = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 0, '<B')
        self._iel = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 1, '<B')
        self._iea = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 2, '<B')
        self._zien = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 5, '<B')
        self._yien = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 6, '<B')
        self._xien = RWRegBit(self._i2c, self._dev_addr, Register.INT_CTRL_REG, 1, 7, '>B')

        self._int = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 0, '>B')
        self._mroi = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 1, '>B')
        self._n_th_s_z = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 2, '>B')
        self._n_th_s_y = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 3, '>B')
        self._n_th_s_x = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 4, '>B')
        self._p_th_s_z = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 5, '>B')
        self._p_th_s_y = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 6, '>B')
        self._p_th_s_x = RORegBit(self._i2c, self._dev_addr, Register.INT_SOURCE_REG, 1, 7, '>B')
        
        self._x = RORegStruct(self._i2c, self._dev_addr, Register.OUTX_L_REG, 2, '<h')
        self._y = RORegStruct(self._i2c, self._dev_addr, Register.OUTY_L_REG, 2, '<h')
        self._z = RORegStruct(self._i2c, self._dev_addr, Register.OUTZ_L_REG, 2, '<h')
        self._temp = RORegStruct(self._i2c, self._dev_addr, Register.TEMP_OUT_L_REG, 2, '<h')
        
        #self._readings = RORegStruct(self._i2c, self._dev_addr, Register.)
        
    @property
    def who_am_i(self):
        return self._who_am_i.__get__()
    
    @property
    def mode(self):
        return self._mode.__get__()
    
    @mode.setter
    def mode(self, value):
        if value>=0 and value<=3:
            self._mode.__set__(value)
        else:
            print('Mode Error - Value out of range')
    
    @property
    def sample_rate(self):
        return self._odr.__get__()
    
    @sample_rate.setter
    def sample_rate(self, value):
        if value>=0 and value<=3:
            self._odr.__set__(value)
        else:
            print('Sample Rate Error - Value out of range')
            
    @property
    def low_power_mode(self):
        return self._lp.__get__()
    
    @low_power_mode.setter
    def low_power_mode(self, value):
        self._lp.__set__(value)
        
    @property
    def soft_reset(self):
        return self._soft_rst.__get__()
        
    @soft_reset.setter
    def soft_reset(self, value):
        self._soft_rst.__set__(value)
        
    @property
    def reboot(self):
        return self._reboot.__get__()
    
    @reboot.setter
    def reboot(self, value):
        self._reboot.__set__(value)
    
    @property
    def temp_comp_en(self):
        return self._comp_temp_en.__get__()
        
    @temp_comp_en.setter
    def temp_comp_en(self, value):
        self._comp_temp_en.__set__(value)

    @property
    def lpf(self):
        return self._lpf.__get__()
    
    @lpf.setter
    def lpf(self, value):
        self._lpf.__set__(value)        
    
    @property
    def offset_cancel(self):
        return self._off_canc.__get__()
        
    @offset_cancel.setter
    def offset_cancel(self, value):
        self._off_canc.__set__(value)
    
    @property
    def set_freq(self):
        return self._set_freq.__get__()
    
    @set_freq.setter
    def set_freq(self, value):
        self._set_freq.__set__(value)
        
    @property
    def int_on_dataoff(self):
        return self._int_on_dataoff.__get__()
    
    @int_on_dataoff.setter
    def int_on_dataoff(self, value):
        self._int_on_dataoff.__set__(value)
            
    @property
    def off_canc_one_shot(self):
        return self._off_canc_one_shot.__get__()
    
    @off_canc_one_shot.setter
    def off_canc_one_shot(self):
        self._off_canc_one_shot.__set__(value)
    
    @property
    def drdy_on_pin(self):
        return self._drdy_on_pin.__get__()
    
    @drdy_on_pin.setter
    def drdy_on_pin(self, value):
        self._drdy_on_pin.__set__(value)
    
    @property
    def self_test(self):
        return self._self_test.__get__()
    
    @self_test.setter
    def self_test(self, value):
        self._self_test.__set__(value)
    
    @property
    def spi4w(self):
        return self._4wspi.__get__()
    
    @spi4w.setter
    def spi4w(self, value):
        self._4wspi.__set__(value)
    
    @property
    def ble(self):
        return self._ble.__get__()
    
    @ble.setter
    def ble(self, value):
        self._ble.__set__(value)
    
    @property
    def bdu(self):
        return self._bdu.__get__()
        
    @bdu.setter
    def bdu(self, value):
        self._bdu.__set__(value)
    
    @property
    def i2c_dis(self):
        return self._i2c_dis.__get__()
    
    @i2c_dis.setter
    def i2c_dis(self, value):
        self.i2c_dis.__set__(value)
    
    @property
    def int_on_pin(self):
        self._int_on_pin.__get__()
        
    @int_on_pin.setter
    def int_on_pin(self, value):
        self._int_on_pin.__set__(value)  
    
    
    @property
    def ien(self):
        return self._ien.__get__()
        
    @ien.setter
    def ien(self, value):
        self._ien.__set__(value)  
    
    @property
    def iel(self):
        return self._iel.__get__()
    
    @iel.setter
    def iel(self, value):
        self._iel.__set(value)
        
    @property
    def iea(self):
        return self._iea.__get__()
    
    @iea.setter
    def iea(self, value):
        self._iea.__set__(value)
    
    @property
    def zien(self):
        return self._zien.__get__()
    
    @zien.setter
    def zien(self, value):
        self._zien.__set__(value)
    
    @property
    def yien(self):
        return self._yien.__get__()
    
    @yien.setter
    def yien(self, value):
        self._yien.__set__(value)
    
    @property
    def xien(self):
        return self._xien.__get__()
    
    @xien.setter
    def xien(self, value):
        self._xien.__set__(value)
    
    @property
    def int(self):
        return self._int.__get__()
    
    @int.setter
    def int(self, value):
        self._int.__set__(value)
    
    @property
    def mroi(self):
        return self._mroi.__get__()
    
    @mroi.setter
    def mroi(self, value):
        self._mroi.__set__(value)
    
    @property
    def n_th_s_z(self):
        return self._n_th_s_z.__get__()
    
    @n_th_s_z.setter
    def n_th_s_z(self, value):
        self._n_th_s_z.__set__(value)
    
    @property
    def n_th_s_y(self):
        return self._n_th_s_y.__get__()
    
    @n_th_s_y.setter
    def n_th_s_y(self, value):
        self._n_th_s_y.__set__(value)
        
    @property
    def n_th_s_x(self):
        return self._n_th_s_x.__get__()
    
    @n_th_s_x.setter
    def n_th_s_x(self, value):
        self._n_th_s_x.__set__(value)

    @property
    def p_th_s_z(self):
        return self._p_th_s_z.__get__()
    
    @p_th_s_z.setter
    def p_th_s_z(self, value):
        self._p_th_s_z.__set__(value)
    
    @property
    def p_th_s_y(self):
        return self._p_th_s_y.__get__()
    
    @p_th_s_y.setter
    def p_th_s_y(self, value):
        self._p_th_s_y.__set__(value)
        
    @property
    def p_th_s_x(self):
        return self._p_th_s_x.__get__()
    
    @p_th_s_x.setter
    def p_th_s_x(self, value):
        self._p_th_s_x.__set__(value)
        
    @property
    def x(self):
        return self._x.__get__()*1.5
    
    @property
    def y(self):
        return self._y.__get__()*1.5
    
    @property
    def z(self):
        return self._z.__get__()*1.5
    
    @property
    def temp(self):
        return self._temp.__get__()/8        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    