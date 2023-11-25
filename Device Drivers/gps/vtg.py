class VTG:
    # Course and speed information relative to the ground
    def init(self):
        self._data
        
    def set_data(self, data):
        self._data = data
        
    def get_course(self):
        # Measured 'True' heading - Degrees
        return self._data[1]
    
    def get_magcourse(self):
        # Measured magnetic heading - Degrees
        return self._data[3]
    
    def get_speed_knots(self):
        # Measured horizontal speed in knots
        return self._data[5]
    
    def get_speed_kmhr(self):
        # Measured horizontal speed in km/hr
        return self._data[7]
    
    def get_mode(self):
        # A - Autonomous
        # D - Differential
        # E - Estimated
        return self._data[9]