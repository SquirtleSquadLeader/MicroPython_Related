class GSA:
    # GPS DOP and Active Satellites
    def __init__(self):
        self._data = []
        
    def set_data(self, nmea_sentence):
        self._data = nmea_sentence
        
    def get_messageid(self):
        return self._data[0]
    
    def get_mode1(self):
        # M - Manual—forced to operate in 2D or 3D mode
        # A - 2D Automatic—allowed to automatically switch 2D/3D
        return self._data[1]
    
    def get_mode2(self):
        # 1 - Fix not available
        # 2 - 2D (＜4 SVs used)
        # 3 - 3D (≧4 SVs used)
        return self._data[2]
    
    def get_sat1(self):
        # Satelite # for channel 1
        return self._data[3]
    
    def get_sat2(self):
        # Satelite # for channel 2
        return self._data[4]
    
    def get_sat3(self):
        # Satelite # for channel 3
        return self._data[5]
    
    def get_sat4(self):
        # Satelite # for channel 4
        return self._data[6]
    
    def get_sat5(self):
        # Satelite # for channel 5
        return self._data[7]
    
    def get_sat6(self):
        # Satelite # for channel 6
        return self._data[8]
    
    def get_sat7(self):
        # Satelite # for channel 7
        return self._data[9]
    
    def get_sat8(self):
        # Satelite # for channel 8
        return self._data[10]
    
    def get_sat9(self):
        # Satelite # for channel 9
        return self._data[11]
    
    def get_sat10(self):
        # Satelite # for channel 10
        return self._data[12]
    
    def get_sat11(self):
        # Satelite # for channel 11
        return self._data[13]
    
    def get_sat12(self):
        # Satelite # for channel 12
        return self._data[14]
    
    def get_pdop(self):
        # Position Dilution of Precision
        return self._data[15]
    
    def get_hdop(self):
        # Horizontal Dilution of Precision
        return self._data[16]
    
    def get_vdop(self):
        # Vertical Dilution of Precision
        return self._data[17]
    
    