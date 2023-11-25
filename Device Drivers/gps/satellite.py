class Satellite:
    def __init__(self, data):
        # Store physical satellite data for GSV class
        self._data = data
        
    @property
    def id(self):
        return self._data[0]
    
    @id.setter
    def id(self, id):
        self._data[0] = id
        
    @property
    def elevation(self):
        return self._data[1]
    
    @elevation.setter
    def elevation(self, elev):
        self._data[1] = elev
        
    @property
    def azimuth(self):
        return self._data[2]
    
    @azimuth.setter
    def azimuth(self, azi):
        self._data[2] = azi
        
    @property
    def sig2noise(self):
        return self._data[3]
    
    @sig2noise.setter
    def sig2noise(self, snr):
        self._data[3] = snr
    