import ustruct
from machine import I2C, Pin

from Register import RWBits, ROBits, ROBytes

# Register Addresses
_MCP9808_CONFIG = const(0x01)
_MCP9808_TUPPER = const(0x02)
_MCP9808_TLOWER = const(0x03)
_MCP9808_TCRIT= const(0x04)
_MCP9808_TA = const(0x05)
_MCP9808_MANU_ID = const(0x06)
_MCP9808_DEV_ID = const(0x07)
_MCP9808_RESOLUTION = const(0x08)

class MCP9808:
    """ This class contains serves to be a driver for the MCP9808 """
    def __init__(self, i2c_bus:I2C, i2c_address:int, mute:bool = True):
        self._i2c_bus = i2c_bus
        self._device_address = i2c_address
        self._mute = mute
        
        if self.addr_check() == True:
            pass
        else:
            print("INSERT ERROR MESSAGE")
            
        """ Registers Objects """
        self._tupper_sign = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TUPPER, 2, 2, 10)
        self._tupper_value = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TUPPER, 2, 2, 10)
        
        self._tlower_sign = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TLOWER, 2, 11, 1)
        self._tlower_value = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TLOWER, 2, 2, 10)
        
        self._tcrit_sign = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TCRIT, 2, 11, 1)
        self._tcrit_value = RWBits(self._i2c_bus, '>H', self._device_address, _MCP9808_TCRIT, 2, 2, 10)
        
        self._ta = ROBytes(self._i2c_bus, '>H', self._device_address, _MCP9808_TA, 2)
        self._device_id = ROBytes(self._i2c_bus, '>H', self._device_address, _MCP9808_DEV_ID, 2)
        self._manu_id = ROBytes(self._i2c_bus, '>H', self._device_address, _MCP9808_MANU_ID, 2)
        self._resolution = RWBits(self._i2c_bus, '>B', self._device_address, _MCP9808_RESOLUTION, 1, 0, 2)
                
    def __str__(self):
        print(f'Device Address: {hex(self._i2c_bus.scan()[0])}\nDevice ID: {self.device_id}')
        print(f'Revision: {self.revision}\nManufacturer ID: {self.manu_id}')
        print(f'Ambient Temp C°: {self.ambient_temp_celsius}')
        print(f'Ambient Temp F°: {self.ambient_temp_fahrenheit}')
        return ''
        
    
    # Methods
    def addr_check(self) -> bool:
        """ Ensure I2C address matches documentation """
        if self._device_address in range(0x18, 0x1F):
            return True
        else:
            print("INSERT ERROR MESSAGE")
        
    # Properties
    @property
    def device_address(self) -> int:
        """

        Returns the I2C device of a particular MCP9808

        :param kind: None
        :type kind: None
        :return: I2C address in hexidecimal format
        :rtype: hex(int)
    
    """
        return hex(self._device_address)
    
    @device_address.setter
    def device_address(self, value:int) -> None:
        """ Sets I2C address and checks for validity """
        self._device_address = value
        self.addr_check()
    
    @property
    def mute(self) -> bool:
        return self._mute
    
    @mute.setter
    def mute(self, value) -> None:
        self._mute = value
    
    @property
    def hi_temperature(self) -> float:
        # Check sign bit
        sign = 1    
        if self._tupper_sign.value == 1:
            sign = -sign
        else:
            pass
        
        # Check value
        temperature = 0
        temp_bits = self._tupper_value.value
        
        for value in range (0, 10):
            if (temp_bits>>value)&0b1 == 0b1:
                temperature += 2**(-2 + value)
                
        return sign * temperature
            
    @hi_temperature.setter
    def hi_temperature(self, value) -> None:
        max_value = 255.75
        min_value = -255.75
        
        # Validate input
        if value > max_value or value < min_value:
            print("Error, value out of bounds")
        if type(value/.25) != int:
            print("Error, value must be multiple of 0.25 C")
        
        # Convert total based on bit resolution
        integer_value = int(value)
        fractional_value = (value - integer_value)/.25
        
        if value == 0:
            self._tupper_sign.value = 0
            self._tupper_value.value  = 0
        elif value > 0:
            self._tupper_sign.value  = 0
            self._tupper_value.value  = (integer_value << 2) + fractional_value
        else:
            self._tupper_sign.value  = 1
            self._tupper_value.value = (integer_value << 2) + fractional_value
    
    @property
    def low_temperature(self) -> float:
        # Check sign bit
        sign = 1    
        if self._tlower_sign.value == 1:
            sign = -sign
        else:
            pass
        
        # Check value
        temperature = 0
        temp_bits = self._tlower_value.value
        
        for value in range (0, 10):
            if (temp_bits>>value)&0b1 == 0b1:
                temperature += 2**(-2 + value)
                
        return sign * temperature
            
    @low_temperature.setter
    def low_temperature(self, value) -> None:
        max_value = 255.75
        min_value = -255.75
        
        # Validate input
        if value > max_value or value < min_value:
            print("Error, value out of bounds")
        if type(value/.25) != int:
            print("Error, value must be multiple of 0.25 C")
        
        # Convert total based on bit resolution
        integer_value = int(value)
        fractional_value = (value - integer_value)/.25
        
        if value == 0:
            self._tlower_sign.value = 0
            self._tlower_value.value  = 0
        elif value > 0:
            self._tlower_sign.value  = 0
            self._tlower_value.value  = (integer_value << 2) + fractional_value
        else:
            self._tlower_sign.value  = 1
            self._tlower_value.value = (integer_value << 2) + fractional_value
    
    @property
    def critical_temperature(self) -> float:         
        # Check value
        temperature = 0
        temp_bits = self._tcrit_value.value        
        
        for value in range (0, 10):
            if (temp_bits>>value)&0b1 == 0b1:
                temperature += 2**(-2 + value)
        
        if self._tcrit_sign.value == 1:
            return -temperature
        else:
            return temperature
            
    @critical_temperature.setter
    def critical_temperature(self, value):
        max_value = 255.75
        min_value = -255.75
        
        # Validate input
        if value > max_value or value < min_value:
            print("Error, value out of bounds")
            
        # if type(value/.25) != int:
        # print("Error, value must be multiple of 0.25 C")
        
        # Convert total based on bit resolution
        integer_value = int(value)
        fractional_value = int((value - integer_value)/.25)
        
        if value == 0:
            self._tcrit_sign.value  = 0
            self._tcrit_value.value  = 0
            
        elif value > 0:
            self._tcrit_sign.value  = 0
            self._tcrit_value.value = (integer_value << 2) + fractional_value

        else:
            self._tcrit_sign.value  = 1
            self._tcrit_value.value = (integer_value << 2) + fractional_value
            
    @property
    def device_id(self):
        """ Returns RO Device ID register value """
        register = self._device_id.value
        device_id = register >> 8 & 0b11111111
        return device_id
    
    @property
    def revision(self):
        """ Returns RO Revision number register value """
        register = self._device_id.value
        revision = register & 0b11111111
        return revision
    
    @property
    def manu_id(self):
        return self._manu_id.value
    
    @property
    def ambient_temp_celsius(self) -> float:
        sign_bit = 12
        sign = 1
        temperature = 0.0
        
        # Store register value
        register_value = self._ta.__get__()
        
        # Determine if temperature is positive or negative
        if (register_value>>sign_bit) & 0b1  == 1:
            sign = -sign
            
        # Determine absolute temperature reading
        temp_bits = register_value&0b111111111111
        
        for value in range (0, 12):
            if (temp_bits>>value)&0b1 == 0b1:
                temperature += 2**(-4 + value)
            
        return temperature * sign

    @property
    def ambient_temp_fahrenheit(self) -> float:
        fahrenheit = self.ambient_temp_celsius*(9/5) + 32
        return fahrenheit
    
    @property
    def resolution(self):
        return self._resolution.value
    
    @resolution.setter
    def resolution(self, value):
        self._resolution.value = value