class RMC:
    # Recommended minimum for navigation
    def __init__(self):
        self._data = []
        
    def set_data(self, nmea_sentence):
        # Sets data, must be parsed and checked prior
        self._data = nmea_sentence
        
    def get_messageid(self):
        # RMC protocol header
        return self._data[0]
        
    def get_utctime(self):
        # hhmmss.sss
        return self._data[1]
    
    def get_status(self):
        # A=data valid or V=data not valid
        return self._data[2]
    
    def get_latitude(self):
        # dmm.mmmm
        return self._data[3]
    
    def get_nsind(self):
        # N=north or S=south
        return self._data[4]
    
    def get_longitude(self):
        # dddmm.mmmm
        return self._data[5]
    
    def get_ewind(self):
        # E=east or W=west
        return self._data[6]
    
    def get_speedoground(self):
        # Knots
        return self._data[7]
    
    def get_courseoground(self):
        # Degrees
        return self._data[8]
    
    def get_date(self):
        # ddmmyy
        return self._data[9]
    
    def get_magvari(self):
        # Degrees
        return self._data[10]
        
    def get_mode(self):
        # A = Autonomous 
        # D = Differential 
        # E = Estimated
        return self._data[11]