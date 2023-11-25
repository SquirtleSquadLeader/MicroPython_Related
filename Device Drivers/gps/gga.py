class GGA:
    # Global Positioning System Fixed Data. Time, Position and fix related data
    def __init__(self):
        self._data = []
        
    def set_data(self, gga_nmea_sentence):
        # Stores latest gga_nmea data - must be checked PRIOR to this call
        self._data = gg_nmea_sentence
        
    def get_messageid(self):
        return self._data[0]
    
    def get_utctime(self):
        # hhmmss.sss
        return self._data[1]
    
    def get_latitude(self):
        #ddmm.mmmm
        return self._data[2]
    
    def get_ns_ind(self):
        # N/S Indicator N N=north or S=south
        return self._data[3]
    
    def get_long(self):
        # ddmm.mmmm
        return self._data[4]
    
    def get_ns_ind(self):
        # E/W Indicator E E=east or W=west
        return self._data[5]
    
    def get_posfix_ind(self):
        # Position Fix Indicator 1 See Table-4
        return self._data[6]
    
    def get_numsats(self):
        # Satellites Used 10 Range 0 to 14
        return self._data[7]
    
    def get_horizdil(self):
        # DDOP 1.00 Horizontal Dilution of Precision
        return self._data[8]
    
    def get_altitudemsl(self):
        # MSL Altitude 8.8 meters Antenna Altitude above/below mean-sea-level
        return self_data[9]
    
    def get_altunits(self):
        # Units M meters Units of antenna altitude
        return self._data[10]
    
    def get_geoidsep(self):
        # Geoidal Separation
        return self._data[11]
    
    def get_geoidunits(self):
        # Units M meters Units of geoids separation
        return self._data[12]
    
    def get_agediffcorr(self):
        # Age of Diff. Corr. second Null fields when DGPS is not used
        return self._data[13]
