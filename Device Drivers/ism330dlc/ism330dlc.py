# MicroPython Standard Library
from micropython import const

# Non-Standard Libraries
import register

class ism330dlc:
    # Registers
    FUNC_CFG_ACCESS = const(0x01)
    SENSOR_SYNC_TIME_FRAME = const(0x04)
    SENSOR_SYNC_RES_RATIO = const(0x05)
    FIFO_CTRL1 = const(0x06)
    FIFO_CTRL2 = const(0x07)
    FIFO_CTRL3 = const(0x08)
    FIFO_CTRL4 = const(0x09)
    FIFO_CTRL5 = const(0x0A)
    DRDY_PULSE_CFG = const(0x0B)
    INT1_CTRL = const(0x0D)
    INT2_CTRL = const(0x0E)
    WHO_AM_I = const(0x0F)
    CTRL1_XL = const(0x10)
    CTRL2_G = const(0x11)
    CTRL3_C = const(0x12)
    CTRL4_C = const(0x13)
    CTRL5_C = const(0x14)
    CTRL6_C = const(0x15)
    CTRL7_G = const(0x16)
    CTRL8_XL = const(0x17)
    CTRL9_XL = const(0x18)
    CTRL10_C = const(0x19)
    MASTER_CONFIG = const(0x1A)
    WAKE_UP_SRC = const(0x1B)
    TAP_SRC = const(0x1C)
    D6D_SRC = const(0x1D)
    STATUS_REG = const(0x1E)
    OUT_TEMP_L = const(0x20)
    OUT_TEMP_H = const(0x21)
    OUTX_L_G = const(0x22)
    OUTX_H_G = const(0x23)
    OUTY_L_G = const(0x24)
    OUTY_H_G = const(0x25)
    OUTZ_L_G = const(0x26)
    OUTZ_H_G = const(0x27)
    OUTX_L_XL = const(0x28)
    OUTX_H_XL = const(0x29)
    OUTY_L_XL = const(0x2A)
    OUTY_H_XL = const(0x2B)
    OUTZ_L_XL = const(0x2C)
    OUTZ_H_XL = const(0x2D)
    SENSORHUB1_REG = const(0x2E)
    SENSORHUB2_REG = const(0x2F)
    SENSORHUB3_REG = const(0x30)
    SENSORHUB4_REG = const(0x31)
    SENSORHUB5_REG = const(0x32)
    SENSORHUB6_REG = const(0x33)
    SENSORHUB7_REG = const(0x34)
    SENSORHUB8_REG = const(0x35)
    SENSORHUB9_REG = const(0x36)
    SENSORHUB10_REG = const(0x37)
    SENSORHUB11_REG = const(0x38)
    SENSORHUB12_REG = const(0x39)
    FIFO_STATUS1 = const(0x3A)
    FIFO_STATUS2 = const(0x3B)
    FIFO_STATUS3 = const(0x3C)
    FIFO_STATUS4 = const(0x3D)
    FIFO_DATA_OUT_L = const(0x3E)
    FIFO_DATA_OUT_H = const(0x3F)
    TIMESTAMP0_REG = const(0x40)
    TIMESTAMP1_REG = const(0x41)
    TIMESTAMP2_REG = const(0x42)
    SENSORHUB13_REG = const(0x4D)
    SENSORHUB14_REG = const(0x4E)
    SENSORHUB15_REG = const(0x4F)
    SENSORHUB16_REG = const(0x50)
    SENSORHUB17_REG = const(0x51)
    SENSORHUB18_REG = const(0x52)
    FUNC_SRC1 = const(0x53)
    FUNC_SRC2 = const(0x54)
    TAP_CFG = const(0x58)
    TAP_THS_6D = const(0x59)
    INT_DUR2 = const(0x5A)
    WAKE_UP_THS = const(0x5B)
    WAKE_UP_DUR = const(0x5C)
    FREE_FALL = const(0x5D)
    MD1_CFG = const(0x5E)
    MD2_CFG = const(0x5F)
    MASTER_CMD_CODE = const(0x60)
    SENS_SYNC_SPI_ERROR_CODE = const(0x61)
    OUT_MAG_RAW_X_L = const(0x66)
    OUT_MAG_RAW_X_H = const(0x67)
    OUT_MAG_RAW_Y_L = const(0x68)
    OUT_MAG_RAW_Y_H = const(0x69)
    OUT_MAG_RAW_Z_L = const(0x6A)
    OUT_MAG_RAW_Z_H = const(0x6B)
    INT_OIS = const(0x6F)
    CTRL1_OIS = const(0x70)
    CTRL2_OIS = const(0x71)
    CTRL3_OIS = const(0x72)
    X_OFS_USR = const(0x73)
    Y_OFS_USR = const(0x74)
    Z_OFS_USR = const(0x75)
    
    def __init__(self, i2c_bus:I2C, address ):
        
        # Data
        self._i2c = i2c_bus
        self._address = address
     
        # Register Objects
        func_cfg_access = RWRegBit(self._i2c, self._address, self.FUNC_CFG_ACCESS, 1, 7, 'B' )










 