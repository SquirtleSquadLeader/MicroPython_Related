"""
    * Author(s): SquirtleSquadLeader
    
    * Dependencies:
        1) MicroPython 
        2) register
        
    * Purpose:
        * The purpose for this driver is to provide control of
        * Invensense MPU-6050 via I2C bus.


    * Notes
    * 1) Set mpu6050.sleep = False to wake up sensor 
    * 2) mpu6050.process_sensors() returns a tuple of all sensor data
    *   a) (xa, ya, za, temp, xg, yg, zg)
           
"""

from machine import I2C
from register import RORegBit, RWRegBit, RORegStruct, RORegBits, RWRegBits
import struct

class Register:
    SMPLRT_DIV = const(25)
    CONFIG = const(26)
    GYRO_CONFIG = const(27)
    ACCEL_CONFIG = const(28)
    FIFO_EN = const(35)
    INT_PIN_CFG = const(55)
    INT_ENABLE = const(56)
    INT_STATUS = const(58)
    ACCEL_XOUT = const(59)
    ACCEL_YOUT = const(61)
    ACCEL_ZOUT = const(63)
    TEMP_OUT = const(65)
    GYRO_XOUT = const(67)
    GYRO_YOUT = const(69)
    GYRO_ZOUT = const(71)
    SIGNAL_PATH_RESET = const(104)
    USER_CTRL = const(106)
    PWR_MGMT_1 = const(107)
    PWR_MGMT_2 = const(108)
    FIFO_COUNT = const(114)
    FIFO_R_W = const(116)
    WHO_AM_I = const(117)
    

class MPU6050:
    
    # Create instance of MPU6050 with valid i2c 
    def __init__(self, i2c_instance, address):
       
        # Bring in instance variables
        self.i2c = i2c_instance
        self.dev_addr = address
        
        
        # Declare register objects
        self._smplrt_div =RWRegBits(self.i2c, self.dev_addr, Register.SMPLRT_DIV, 1, 0, 7, '>B')
        
        self._dlpf_cfg = RWRegBits(self.i2c, self.dev_addr, Register.CONFIG, 1, 0, 2, '>B')
        self._ext_sync_set = RWRegBits(self.i2c, self.dev_addr, Register.CONFIG, 1, 3, 5, '>B')
        
        self._fs_sel = RWRegBits(self.i2c, self.dev_addr, Register.GYRO_CONFIG, 1, 3, 4, '>B')
        
        self._afs_sel = RWRegBits(self.i2c, self.dev_addr, Register.ACCEL_CONFIG, 1, 3, 4, '>B')
        
        self._accel_fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.FIFO_EN, 1, 3, '>B')
        self._zg_fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.FIFO_EN, 1, 4, '>B')
        self._yg_fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.FIFO_EN, 1, 5, '>B')
        self._xg_fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.FIFO_EN, 1, 6, '>B')
        self._temp_fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.FIFO_EN, 1, 7, '>B')
        
        self._i2c_bypass_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 1, '>B')
        self._fsync_int_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 2, '>B')
        self._fsync_int_level = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 3, '>B')
        self._int_rd_clear = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 4, '>B')
        self._latch_int_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 5, '>B')
        self._int_open = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 6, '>B')
        self._int_level = RWRegBit(self.i2c, self.dev_addr, Register.INT_PIN_CFG, 1, 7, '>B')
        
        self._data_rdy_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_ENABLE, 1, 0, '>B')
        self._i2c_mst_int_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_ENABLE, 1, 3, '>B')
        self._fifo_oflow_en = RWRegBit(self.i2c, self.dev_addr, Register.INT_ENABLE, 1, 4, '>B')
        
        self._data_rdy_int = RORegBit(self.i2c, self.dev_addr, Register.INT_STATUS, 1, 0, '>B')
        self._i2c_mst_int_int = RORegBit(self.i2c, self.dev_addr, Register.INT_STATUS, 1, 3, '>B')
        self._fifo_oflow_int = RORegBit(self.i2c, self.dev_addr, Register.INT_STATUS, 1, 4, '>B')
        
        self._accel_x = RORegStruct(self.i2c, self.dev_addr, Register.ACCEL_XOUT, 2, '>h')
        self._accel_y = RORegStruct(self.i2c, self.dev_addr, Register.ACCEL_YOUT, 2, '>h')
        self._accel_z = RORegStruct(self.i2c, self.dev_addr, Register.ACCEL_ZOUT, 2, '>h')
        
        self._temp = RORegStruct(self.i2c, self.dev_addr, Register.TEMP_OUT, 2, '>h')
        
        self._gyro_x = RORegStruct(self.i2c, self.dev_addr, Register.GYRO_XOUT, 2, '>h')
        self._gyro_y = RORegStruct(self.i2c, self.dev_addr, Register.GYRO_YOUT, 2, '>h')
        self._gyro_z = RORegStruct(self.i2c, self.dev_addr, Register.GYRO_ZOUT, 2, '>h')
        
        self._temp_reset = RWRegBit(self.i2c, self.dev_addr, Register.SIGNAL_PATH_RESET, 1, 0, '>B')
        self._accel_reset = RWRegBit(self.i2c, self.dev_addr, Register.SIGNAL_PATH_RESET, 1, 1, '>B')
        self._gyro_reset = RWRegBit(self.i2c, self.dev_addr, Register.SIGNAL_PATH_RESET, 1, 2, '>B')
        
        self._sig_cond_reset = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 0, '>B')
        self._i2c_mst_reset = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 1, '>B')
        self._fifo_reset = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 2, '>B')
        self._i2c_if_dis = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 4, '>B')
        self._i2c_mst_en = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 5, '>B')
        self._fifo_en = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 6, '>B')  
        
        self._clksel = RWRegBits(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 0, 2, '>B')
        self._temp_dis = RWRegBit(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 3, '>B')
        self._cycle = RWRegBit(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 5, '>B')
        self._sleep = RWRegBit(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 6, '>B')
        self._device_reset = RWRegBit(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 7, '>B')
        
        self._stby_zg = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 0, '>B')
        self._stby_yg = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 1, '>B')
        self._stby_xg = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 2, '>B')
        self._stby_za = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 3, '>B')
        self._stby_ya = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 4, '>B')
        self._stby_xa = RWRegBit(self.i2c, self.dev_addr, Register.USER_CTRL, 1, 5, '>B')
        self._lp_wake_ctrl = RWRegBits(self.i2c, self.dev_addr, Register.PWR_MGMT_1, 1, 6, 7, '>B')
        
        self._who_am_i = RORegBits(self.i2c, self.dev_addr, Register.WHO_AM_I, 1, 0, 6)
        
        # Declare settings to reduce I2C transactions        
        self.accel_scale = 16384 / (2**self.afs_sel)
        self.gyro_scale =  131 / (2**self.fs_sel) 
        
        self.sleep = False
       
        
    # === Property ===
    @property
    def sample_rate(self):
        return self._smplrt_div.__get__()
    
    @sample_rate.setter
    def sample_rate(self, value):
        if value>=0 and value<=256:
            self._smplrt_div.__set__(value)
        else:
            print('Sample Rate Error - Value out of range')
            
    @property
    def dlpf(self):
        return self._dlpf_cfg.__get__()
    
    @dlpf.setter
    def dlpf(self, value):
        if value>=0 and value<=7:
            self._dlpf_cfg.__set__(value)
        else:
            print('DLPF Error - Value out of range')
            
    @property
    def ext_sync(self):
        return self._ext_sync_set.__get__()
    
    @ext_sync.setter
    def ext_sync(self, value):
        if value>=0 and value<=7:
            self._ext_sync_set.__set__(value)
        else:
            print('External Sync Set Error - Value out of range')
            
    @property
    def fs_sel(self):
        return self._fs_sel.__get__()
    
    @fs_sel.setter
    def fs_sel(self, value):
        if value>=0 and value<=3:
            self._fs_sel.__set__(value)
            self.gyro_scale = 131 / (2**self.fs_sel) 
        else:
            print('FS_SEL Error - Value out of range')
            
    @property
    def afs_sel(self):
        return(self._afs_sel.__get__())
    
    @afs_sel.setter
    def afs_sel(self, value):
        if value>=0 and value<=3:
            self._afs_sel.__set__(value)
            self.accel_scale = 16384 / (2**value)
        else:
            print('AFS_SEL Error - Value out of Range')
            
    @property
    def i2c_bypass_en(self):
        return self._i2c_bypass_en.__get__()
    
    @i2c_bypass_en.setter
    def i2c_bypass_en(self, value):
        self._i2c_bypass_en.__set__(value)
        
    @property
    def fsync_int_en(self):
        return self._fsync_int_en.__get__()
        
    @fsync_int_en.setter
    def fsync_int_en(self, value):
        self._fsync_int_en.__set__(value)
        
    @property
    def int_rd_clear(self):
        return self._int_rd_clear.__get__()
        
    @int_rd_clear.setter
    def int_rd_clear(self, value):
        self._int_rd_clear.__set__(value)
        
    @property
    def latch_int_en(self):
        return self._latch_int_en.__get__()
    
    @latch_int_en.setter
    def latch_int_en(self, value):
        self._latch_int_en.__set__(value)
    
    @property
    def int_open(self):
        return self._int_open.__get__()
    
    @int_open.setter
    def int_open(self, value):
        self._int_open.__set__(value)
        
    @property
    def int_level(self):
        return self._int_level.__get__()
    
    @int_level.setter
    def int_level(self, value):
        self._int_level.__set__(value)
        
    @property
    def data_rdy_en(self):
        self._data_rdy_en.__get__()
    
    @data_rdy_en.setter
    def data_rdy_en(self, value):
        self._data_rdy_en.__set__(value)
    
    @property
    def data_rdy_int(self):
        self._data_rdy_int.__get__()
    
    @property
    def accel_x(self):
        return(self._accel_x.__get__()/(self.accel_scale))
    
    @property
    def accel_y(self):
        return(self._accel_y.__get__()/(self.accel_scale))
    
    @property
    def accel_z(self):
        return(self._accel_z.__get__()/(self.accel_scale))
    
    @property
    def temp(self):
        return((self._temp.__get__()/340)+36.53)
    
    @property
    def gyro_x(self):
        return(self._gyro_x.__get__()/(self.gyro_scale))
    
    @property
    def gyro_y(self):
        return(self._gyro_y.__get__()/(self.gyro_scale))
    
    @property
    def gyro_z(self):
        return(self._gyro_z.__get__()/(self.gyro_scale))
    
    @property
    def temp_reset(self):
        return self._temp_reset.__get__()
    
    @temp_reset.setter
    def temp_reset(self, value):
        self._temp_reset.__set__(value)
    
    @property
    def accel_reset(self):
        return self._accel_reset.__get__()
    
    @accel_reset.setter
    def accel_reset(self, value):
        self._accel_reset.__set__(value)
    
    @property
    def gyro_reset(self):
        return self._gyro_reset.__get__()
    
    @gyro_reset.setter
    def gyro_reset(self, value):
        self._gyro_reset.__set__(value)
    
    @property
    def sig_cond_reset(self):
        return self._sig_cond_reset.__get__()
    
    @sig_cond_reset.setter
    def sig_cond_reset(self, value):
        self._sig_cond_reset.__set__(value)
        
    @property
    def clksel(self):
        return self._clksel.__get__()
        
    @clksel.setter
    def clksel(self, value):
        if value>=0 and value<=7:
            self._clksel.__set__(value)
        else:
            print('CLKSEL Error - Value out of range')
    
    @property
    def temp_dis(self):
        return self._temp_dis.__get__()
    
    @temp_dis.setter
    def temp_dis(self, value):
        self._temp_dis.__set__(value)
        
    @property
    def cycle(self):
        return self._cycle.__get__()
    
    @cycle.setter
    def cycle(self, value):
        self._cycle.__set__(value)
    
    @property
    def sleep(self):
        return self._sleep.__get__()
    
    @sleep.setter
    def sleep(self, value):
        self._sleep.__set__(value)
    
    @property
    def device_reset(self):
        return self._device_reset.__get__()
        
    @device_reset.setter
    def device_reset(self, value):
        self._device_reset.__set__(value)
        
    @property
    def stby_zg(self):
        return self._stby_zg.__get__()
        
    @stby_zg.setter
    def stby_zg(self, value):
        self._stby_zg.__set__(value)
    
    @property
    def stby_yg(self):
        return self._stby_yg.__get__()
    
    @stby_yg.setter
    def stby_yg(self):
        self._stby_yg.__set__(value)
    
    @property
    def stby_xg(self):
        return self._stby_xg.__get__()
    
    @stby_xg.setter
    def stby_xg(self):
        self._stby_xg.__set__(value)
    
    @property
    def stby_za(self):
        return self._stby_za.__get__()
    
    @stby_za.setter
    def stby_za(self, value):
        self._stby_za.__set__(value)
    
    @property
    def stby_ya(self):
        return self._stby_ya.__get__()
    
    @stby_ya.setter
    def stby_ya(self, value):
        self._stby_ya.__set__(value)
        
    @property
    def stby_xa(self):
        return self._stby_xa.__get__()
    
    @stby_xa.setter
    def stby_xa(self, value):
        self._stby_xa.__set__(value)
    
    @property
    def lp_wake_ctrl(self):
        return self._lp_wake_ctrl.__get__()
        
    @lp_wake_ctrl.setter
    def lp_wake_ctrl(self, value):
        if value>=0 and value<=3:
            self._lp_wake_ctrl.__set__(value)
        else:
            print('LP_Wake_Ctrl Error - Value out of range')
            
    @property
    def who_am_i(self):
        return self._who_am_i.__get__()
        
    # Functions
    def read_sensors(self):        
        return(self.i2c.readfrom_mem(self.dev_addr, Register.ACCEL_XOUT, 14))
    
    def unpack_sensors(self):
        return list(struct.unpack('>hhhhhhh', self.read_sensors()))
    
    def process_sensors(self):
        list_of_values = self.unpack_sensors()

        # Accel's
        for value in range(0,3):
            list_of_values[value] = list_of_values[value] / self.accel_scale
        
        # Temp
        list_of_values[3] = (list_of_values[3]/340)+36.53
        
        # Gyro's
        for value in range(4,7):
            list_of_values[value] = list_of_values[value] / self.gyro_scale
        
        return list_of_values
    
    def pack_sensors(self):
        list_of_values = self.process_sensors()
        array_of_values =  struct.pack('>fffffff', *list_of_values)
        return array_of_values
