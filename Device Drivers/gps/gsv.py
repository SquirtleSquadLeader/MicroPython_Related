from gps.satellite import Satellite

class GSV:
    # Satellites in View
    def __init__(self):
        self._sats = []
        
    def clear_data(self):
        # Clear data
        self._sats = []
        
    def add_satellite(self, nmea_sentence):
        # Parse nmea_sentence into Satellite objects 
        sat1 = Satellite(nmea_sentence[4:7])
        sat2 = Satellite(nmea_sentence[8:11])
        sat3 = Satellite(nmea_sentence[12:15])
        
        # Add satellite objects into list
        self._sats.append(sat1)
        self._sats.append(sat2)
        self._sats.append(sat3)
        
    def loc_sat_inlist(self, sat_channel):
        # Find satelite channel to get data from
        # Satellite ID / Channel (Range 1 to 32)
        for sat in range(0, len(self._sats)):
            if self._data[sat].id ==  sat_channel:
                return sat
            
    def get_sat(self, sat_num):
        # Returns Satellite object for interaction
        return self._sats[sat_num]
        
        
    