"""
    * Author(s): SquirtleSquadLeader
    
    * Dependencies:
    *   1) MicroPython
        
    * Purpose:
        * The purpose of this module is to provide easy I2C Register
        * access.  It is inspired by the CircuitPython Register
        * module maintained by Adafruit.
        
            * RORegBit - Single bit Read Only 
            * RWRegBit - Single bit Read/Write
            
            * RORegBits - Multi-bit Read Only
            * RWRegBits - Multi-bit Read/Write
            
            * RORegStruct - C-Types Read Only
            * RWRegStruct - C-Types Read/Write
            
        
    * Notes:
        1) Reference format strings below:                   
             Format          C Type          Standard size    
                c         char                    1
                b         signed char             1
                B         unsigned char           1
                h         short                   2
                H         unsigned short          2
                i         integer                 4
                I         unsigned int            4
                l         long                    4
                L         unsigned long           4
                q         long long               8
                Q         unsigned long long      8
                f         float                   4
                d         double                  8
        
"""

from machine import I2C
import struct

class RORegBit:
    def __init__(self, i2c, dev_addr, reg_addr, num_bytes, bit_location, fmt_str):
        self.i2c = i2c
        self.dev_addr = dev_addr
        self.reg_addr = reg_addr
        self.num_bytes = num_bytes
        self.bit_location = bit_location
        self.pre_bits = 0
        self.fmt_str = fmt_str
        
        for bit in range(0,(self.bit_location-1)):
            self.pre_bits = self.pre_bits+1
    
    def __get__(self):
        # Retrieve register value and unpack to int
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)
        
        # Perform shift followed by _AND_ operation to determine bit state
        bit_value = (value >> self.bit_location)&1
        
        return bit_value
    
class RWRegBit:
    def __init__(self, i2c, dev_addr, reg_addr, num_bytes, bit_location, fmt_str):
        self.i2c = i2c
        self.dev_addr = dev_addr
        self.reg_addr = reg_addr
        self.num_bytes = num_bytes
        self.bit_location = bit_location
        self.fmt_str = fmt_str
        self.premask = 0
        
        # Masking for values prior to desired bitfield... if needed
        if self.bit_location > 0:
            for bit in range(0, self.bit_location):
                self.premask = self.premask + 2**bit
    
    def __get__(self):
        # Retrieve register value and unpack to int
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)
        
        # Perform shift followed by _AND_ operation to determine bit state        
        return (value >> self.bit_location)&1
    
    def __set__(self, bit_value):
        # Retrieve register value and unpack as int
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)

        # Pack to bytes object
        new_value = (value>>(self.bit_location+1)) + (bit_value<<self.bit_location) + (value&self.premask)
        new_value = struct.pack(self.fmt_str, new_value)
        
        # Write to I2C
        self.i2c.writeto_mem(self.dev_addr, self.reg_addr, new_value)
        
class RORegBits:
    def __init__(self, i2c, dev_addr, reg_addr, num_bytes, lsb, msb):
        self.i2c = i2c
        self.dev_addr = dev_addr
        self.reg_addr = reg_addr
        self.num_bytes = num_bytes
        self.lsb = lsb
        self.msb = msb
        self.width = msb - lsb
        self.mask = 1
        
        # Generate bitmask
        for bit in range(0, self.width):
            self.mask = (self.mask<<1) + 1
            
        # Locate mask
        self.mask = self.mask << self.lsb
        
    def __get__(self):
        # Return value of bitfield
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)        
        return value & self.mask
        
class RWRegBits:
    def __init__(self, i2c, dev_addr, reg_addr, num_bytes, lsb, msb, fmt_str):
        self.i2c = i2c
        self.dev_addr = dev_addr
        self.reg_addr = reg_addr
        self.num_bytes = num_bytes
        self.lsb = lsb
        self.msb = msb
        self.fmt_str = fmt_str
        self.mask = 0
        self.premask = 0
        
        # Masking for bitfield that will be over written
        for bit in range(0, (self.msb-self.lsb+1)):
            self.mask = self.mask + 2**bit
        
        # Masking for values prior to desired bitfield... if needed
        if self.lsb > 0:
            for bit in range(0, self.lsb-1):
                self.premask = self.premask + 2**bit
        
    def __get__(self):
        # Retrieve register value and unpack to int
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)        
        return (value >> self.lsb)&self.mask
    
    def __set__(self, setting):
        [value] = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)
        
        new_value = ((value>>(self.msb+1))<<(self.msb+1)) + (setting<<self.lsb) + (value&self.premask)
        
        """
        post = value>>(self.msb+1)
        pre = value&self.premask
        #print('Start: ', bin(value))
        #print('Pre:', post)
        #print('Value: ', (setting<<self.lsb))
        #print('Post: ', pre)
        new_value = post + (setting<<self.lsb) + pre
        #print('End: ', bin(new_value))
        """
        new_value = struct.pack(self.fmt_str, new_value)        
        self.i2c.writeto_mem(self.dev_addr, self.reg_addr, new_value)        
        
class RORegStruct:
    def __init__(self, i2c, dev_addr, reg_addr, num_bytes, fmt_str):
        self.i2c = i2c
        self.dev_addr = dev_addr
        self.reg_addr = reg_addr
        self.num_bytes = num_bytes
        self.fmt_str = fmt_str
    
    def __get__(self):
        value = self.i2c.readfrom_mem(self.dev_addr, self.reg_addr, self.num_bytes)
        real_value = struct.unpack(self.fmt_str, value)
        return real_value[0]

class RO_Transaction:
    """
    The user can supply a transaction object with a list of any number of
    Register objects. The Transaction object will then perform one I2C
    transaction and return all data as a list OR perform all write operations.
    
    1) The Register objects should all be from one physical I2C device
    2) True = Read, False = Write (Default is read)
    3) Reads can be from non-sequential registers
    4) Writes can be made only to sequential registers OR more than one
       transaction will be generated
    
    i.e.
    
    # Define Register objects
    register1 = [ROBits Object]
    register2 = [ROBits Object]
    register3 = [ROBits Object]
    
    # Create list object containing only Register objects
    list_of_registers = [register1, register2, register3]
    
    # Instantiate Transaction object
    data_from_device = Transaction(list_of_registers)
    
    # Retrieve data
    data = data_from_device.__get__()
    
    # Use data as desired
    datapoint_1 = data_from_device[0]
    datapoint_2 = data_from_device[1]
    datapoint_3 = data_from_device[2]
    """
    
    def __init__(self, read_or_write:bool = True, list_of_registers:list() =[]):
        # Data
        self._list_of_registers = list_of_registers
        
        # Check container type
        if self._list_of_registers.__class__() == list():
            
            # Check each element against all possible Register types
            for reg in self._list_of_registers:
                if self._list_of_registers[reg].__class__() in [RORegBit, RORegBits, RWRegBit, RWRegBits, RORegStruct]:
                    pass
                else:
                    # Error
                    pass
                
    def add_reg(self, reg_object):
        """
        This function allows for register objects to be added to an already
        instantiated Transaction object
        """
        if reg_object.__class__() in [RORegBit, RORegBits, RWRegBit, RWRegBits, RORegStruct]:
            self._list_of_registers.append(reg_object)
        else:
            # Error
            pass
        
    def rem_reg(self, reg_object):
        """
        This function allows for a register object to be removed from an
        already instantiated transaction object
        """
        if reg_object.__class__() in [RORegBit, RORegBits, RWRegBit, RWRegBits, RORegStruct]:
            self._list_of_registers.remove(reg_object)
        else:
            # Error
            pass
        
    def order_list(self):        
        """
        1) Inspect each register to verify all the same device
        2) Order register objects in ascending register location 0x0000... 0xffff
        3) Perform single I2C Read from LowReg - HighReg location
        4) Iterate through list and unpack data using Register Object data
        
        reg_addresses  = []
        
        for reg in self._list_of_registers:
            reg_addresses.append(self._list_of_registers[reg].reg_address)
            
        """
        pass
            
        
            
            
        
            
                 
        
                 
        
        