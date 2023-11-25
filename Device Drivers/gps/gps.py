# Pystd & uPystd
from machine import UART, Pin
import time

# GPS
from gps.gga import GGA
from gps.rmc import RMC
from gps.gsa import GSA
from gps.gsv import GSV
from gps.vtg import VTG

class Datum:
    #  330 PMTK_API_SET_DATUM
    WGS64 = '0*2E'    
    
class UpdateRate:
    RATE_1HZ = '1000*1F'
    RATE_5HZ = '200*2C'
    RATE_10HZ = '100*2F'
    
class Baudrate:
    # 251 PMTK_SET_NMEA_BAUDRATE
    BAUD_4800 = '4800*14'
    BAUD_9600 = '9600*17'
    BAUD_14400 = '14400*29'
    BAUD_19200 = '19200*22'
    BAUD_38400 = '38400*27'
    BAUD_57600 = '57600*2C'
    BAUD_115200 = '115200*1F'
    
class DGPS_Source:
    # 301 PMTK_API_SET_DGPS_MODE
    DGPS_OFF = '0*2C'
    DGPS_RTCM = '1*2D'
    DGPS_WAAS = '2*2E'
    
class NAV_Threshold:
    NT_0_2 = '0.20*02'
    NT_0_4 = '0.4*34'
    NT_0_6 = '0.6*36'
    NT_0_8 = '0.8*38'
    NT_1_0 = '1.0*31'
    NT_1_5 = '1.5*34'
    NT_2_0 = '2.00*02'
    
class GPS:
    """
    GPS Driver for: Adafruit Ultimate GPS Breakout v3        
    """
    MAX_PACKET_LENGTH = 255
    
    PREAMBLE = '$'
    TALKERID = 'PMTK'
    
    # Packet Type
    PMTK_ACK = '001'
    PMTK_SYS_MSG = '010'
    PMTK_TXT_MSG = '011'
    PMTK_CMD_HOT_START = '101'
    PMTK_CMD_WARM_START = '102'
    PMTK_CMD_COLD_START = '103'
    PMTK_CMD_FULL_COLD_START = '104'
    PMTK_SET_NMEA_UPDATERATE = '220'
    PMTK_SET_NMEA_BAUDRATE = '251'
    PMTK_API_SET_DGPS_MODE = '301'
    PMTK_API_Q_DGPS_MODE = '401'
    PMTK_API_DT_DGPS_MODE = '501'
    PMTK_API_SET_SBAS_ENABLED = '313'
    PMTK_API_Q_SBAS_ENABLED = '413'
    PMTK_DT_SBAS_ENABLED = '513'
    PMTK_API_SET_NMEA_OUTPUT = '314'
    PMTK_API_Q_NMEA_OUTPUT = '414'
    PMTK_API_DT_NMEA_OUTPUT = '514'
    PMTK_API_SET_SBAS_Mode = '319'
    PMTK_API_Q_SBAS_Mode = '419'
    PMTK_API_DT_SBAS_Mode = '519'
    PMTK_Q_RELEASE = '605'
    PMTK_DT_RELEASE = '705'
    PMTK_Q_EPO_INFO = '607'
    PMTK_DT_EPO_INFO = '707'
    PMTK_CMD_CLEAR_EPO = '127'
    PMTK_SET_NAV_397 = '397'
    PMTK_SET_NAV_386 = '386'
    PMTK_Q_NAV_THRSHLD = '447'
    PMTK_DT_NAV_THRSHLD = '527'
    PMTK_CMD_STANDBY_MODE = '161'
    PMTK_SET_AL_DEE_CFG = '232'
    PMTK_CMD_PERIODIC_MODE = '225'
    PMTK_CMD_AIC_MODE = '286'
    PMTK_CMD_EASY_ENABLE = '896'
    PMTK_LOCUS_CONFIG = '187'
    PMTK_API_SET_DATUM = '330'
    PMTK_API_Q_DATUM = '430'
    PMTK_API_DT_DATUM = '530'
    PMTK_API_SET_SUPPORT_QZSS_NMEA = '351'
    PMTK_API_SET_STOP_QZSS = '352'
    
    STAR = '*'    
    END_OF_PACKET = '\r\n'
    
    
    def __init__(self, uart, fix_pin, pps_pin, en_pin):
        
        # Class data
        self._uart = uart
        self._fix_pin = fix_pin
        self._pps_pin = pps_pin
        self._en_pin = en_pin
        self._data_ready = False
        self._data_buffer = None
        self._last_fix = 0
        self._curr_fix = 0
        self._last_pps = 0
        self._curr_pps = 0
        
        # NMEA Class objects
        self._gga = GGA()
        self._rmc = RMC()
        self._vtg = VTG()
        self._gsv = GSV()
        
        # Pin definitions
        """
        self._pps = Pin(PULSE_PERSECOND, Pin.IN)
        self._fix = Pin(FIX, Pin.IN)
        self._gps_en = Pin(GPS_ENABLE, Pin.OUT)
        """
        
    def __str__(self):
        return self.readall()
    
    def read(self):
        # Return one line from UART buffer, if possible
        try:
            if self._uart.any() > 0:
                return self._uart.readline().decode()
            else:
                return None
        except:
            # Error Handling
            pass
    
    def readall(self):
        # Return all lines from UART buffer
        try:
            if self._uart.any() > 0:
                return self._uart.read(self._uart.any()).decode()
            else:
                return None
        except:
            # Error Handling
            pass
        
    def printall(self):
        print(self.readall())
        
    def printall_byline(self):
        while self._uart.any() > 0:
            print(self._uart.any(),' ',self._uart.readline())
    
    def service_routine(self):
        self._data_ready = True
        
    def print_data(self):
        print(self.readall())
        self._data_ready = False
    
    def send_command(self, packet_type, data:str = ''):
        checksum_packet = GPS.TALKERID + packet_type + data
        command_packet = GPS.PREAMBLE + checksum_packet + GPS.STAR + self.calc_checksum(checksum_packet) + GPS.END_OF_PACKET

        self._uart.write(command_packet)
            
    def flush(self):
        self._uart.flush()
    
    def enable(self):
        self._en_pin.on()
        
    def disable(self):
        self._en_pin.off()
        
    def sort_sentence(self, sentence):
        """
        This function takes in a checksum verified NMEA sentence and forwards it to the appropriate
        function to store the data in the class.
        """
        
        fragment_small = sentence[2:5]
        fragment_large = sentence[0:4]
        fragment_large_id = sentence[4:7]
        
        if fragment_large == 'PMTK':
            # Ack, System Message, or other output from hardware
            if fragment_large_id == '001':
                # Ack
                self.parse_ack(sentence)
                
            elif fragment_large_id == '010':
                # System Message
                self.parse_sys_msg(sentence)
                
            elif fragment_large_id == '011':
                # Text Message
                #self.parse_sys_msg(sentence)
                pass
            
        elif fragment_small == 'GGA' :
            # Time, position and fix type data
            self.parse_gga(sentence)
            
        elif fragment_small == 'RMC':
            # Time, date, position, course and speed data. Recommended Minimum Navigation Information.
            self.parse_rmc(sentence)
            
        elif fragment_small == 'VTG':
             # Course and speed information relative to the ground.
            self.parse_vtg(sentence)
            
        elif fragment_small == 'GSA':
             # GPS receiver operating mode, active satellites used in the position solution and DOP values.
             self.parse_gsa(sentence)
             
        elif fragment_small == 'GSV':
             # The number of GPS satellites in view satellite ID numbers, elevation, azimuth, and SNR values.
             self.parse_gsv(sentence)            
        else:
            # Incomplete/Unknown NMEA Sentence
            return False
        
    def parse_ack(self, sentence):           
        # Process acknowledgment messages
        pass
        
    def parse_sys_msg(self, sentence):           
        # Process system messages
        pass
    
    def parse_sys_msg(self, sentence):           
        # Process text messages
        pass
        
    def parse_gga(self, sentence):
        # Parse GGA data into sub components
        self._last_gga = sentence.split(',')
        #print('GGA stored in memory')
        
    def parse_rmc(self, sentence):
        # Parse RMC data into sub components
        self._last_rmc = sentence.split(',')
        #print('RMC stored in memory')
        
    def parse_vtg(self, sentence):
        # Parse VTG data into sub components
        self._last_vtg = sentence.split(',')
        #print('VTG stored in memory')
        
    def parse_gsa(self, sentence):
        # Parse GSA data into sub components
        self._last_gsa = sentence.split(',')
        #print('GSA stored in memory')
        
    def parse_gsv(self, sentence):
        # Parse GSV data into sub components
        self._last_gsv = sentence.split(',')
        #print('GSV stored in memory')
    
    def verify_output(self, sentence):
        try:
            # Acquire Hex checksum from sentence
            #print(sentence)
            start = len(sentence)-4
            end = len(sentence)-2
            sentence_checksum = sentence[start:end]
            sentence_checksum = int('0x' + sentence_checksum)
            
            verification_checksum = 0
            
            # Repeat Xor for characters between $ and *
            for char in range(0, (len(sentence)-5)):
                verification_checksum ^= ord(sentence[char])
            
            # Return based upon findings
            if verification_checksum == sentence_checksum:
                return True
            else:
                return False
        
        except:
            # Error Handling
            pass
        
        
        
    def calc_checksum(self, sentence):
        # Used to determine checksum value for custom messages
        checksum = 0
        
        # Move through characters and Xor against itself
        for char in range(0, len(sentence)):
            checksum^=ord(sentence[char])
        
        # Get hexidecimal representation and trim 
        checksum = hex(checksum)[2:]
        
        return checksum
    
    def cold_restart(self):
        self.send_command(GPS.PMTK_CMD_FULL_COLD_START,)
        return True
            
    @property
    def data_ready(self):
        return self._data_ready

    @data_ready.setter
    def data_ready(self, value):
        self._data_ready = value
    
    def get_datum(self):
        # Return datum in use
        command = '$PMTK430*35\r\n'
        self._uart.write(command)
        datum = self._uart.readline()
        return datum
    
    def standby_enable(self):
        # Device stop updating data, UART continues to populate - saves power
        self.send_command(PMTK_CMD_STANDBY_MODE, 0*28)
        
    def standby_disable(self):
        # Device returns to configured operation
        self._uart.write('A\r\n')
        
    def set_navthresh(self, setting):
        # Sets threshold speed when navigation
        pass
        
    def output_config(self):
        # Set which NMEA sentences are output
        self.send_command(GPS.PMTK_API_SET_NMEA_OUTPUT ,'1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29')