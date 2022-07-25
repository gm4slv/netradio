'''
Python NMEA Radio Functions module for Icom IC-M710 Marine HF SSB Transceiver

    Copyright (C) 2015  John Pumford-Green

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# serial port for Icom IC-M710 Rig Control

import serial
import threading
import time
version = "v0.1"

sport = '/dev/ttyUSB0'
sbaud = 4800

#ser = serial.Serial(sport, 4800, timeout=1)
lock = threading.Lock()

# NMEA Codes
preamble = "$PICOA,"
controller = "90"
radio = "01" 
cr = "\x0d"
lf = "\x0a"


# Commands are sent as NMEA private sentences:
#
# $PICOA,controller_id,radio_id,command,<parameter>,*HH<CR><LF>
#
# where HH is the 2 digit ECC value below:
#
# The protocol document states that for messages FROM the controller TO the radio
# the ECC bytes are optional, and may be omitted. This appears to be false information, and
# the ECC bytes seem to be necessary.
#
# The ECC checksum, is a two-digit hex value found by XORing the hex values of the characters 
# between "$" and "*" (but not including the $ or *)
#
# The first part of the message is always:
# "PICOA,90,01," and this has an XOR value of (decimal) 112
# we then XOR this with each character's decimal ASCII value, in the required command
# and convert the result to a 2-digit hex value
#

class m710(object):
    def __init__(self, model):
        self.ser = serial.Serial(sport, sbaud, timeout=0.1)
        self.model = model


    def get_ecc(self,command):
        ecc = 112
        for c in command:
            ecc = ord(c) ^ ecc
        hecc = '{0:02x}'.format(int(ecc))
        
        return hecc

# we must force the radio into "Remote" mode before sending any other commands.    
    def remote_on(self):
        command = "REMOTE,ON"
        ecc = self.get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            return
        else:
            return self.remote_on()
    
        

# we can leave the radio in "Remote" mode for as long as we want to control it remotely
# but we must close the "Remote" mode when finished. The previous radio settings (channel/power etc) are
# restored after Remote mode is closed.
    def remote_off(self):
        command = "REMOTE,OFF"
        ecc = self.get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr) 
        if result:
            #ser.close()
            return
        else:
            return self.remote_off()
    

    def ptt_on():
        command = "TRX,TX"
        ecc = get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return
        else:
            return ptt_on()

    def ptt_off():
        command = "TRX,RX"
        ecc = get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return
        else:
            return ptt_off()



    def get_freq(self):
        fkhz = self.get_rxfreq()
        #fkhz = "%.3f" % (float(f) * 1000)
        return fkhz

    def set_freq(self,freq):
        
        self.set_rxfreq(freq)
        self.set_txfreq(freq)
        return "Set freq success"
            
    def get_rxfreq(self):
        command = "RXF"
        ecc = self.get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            list = result.split(",")
            f = list[4].split("*")[0]
            fkhz = "%.3f" % (float(f) * 1000)
            return fkhz
        else:
            return self.get_rxfreq()
        
        
    def get_txfreq(self):
        command = "TXF"
        ecc = get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            list = result.split(",")
            f = list[4].split("*")[0]
            fkhz = "%.3f" % (float(f) * 1000)
            return fkhz
        else:
            return self.get_txfreq()
        

    def get_mode(self):
        command = "MODE"
        ecc = self.get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            list = result.split(",")
            mode = list[4].split("*")[0]
            if mode == "J2B":
                mode = "DATA"
            return mode
        else:
            return self.get_mode()
        
       

    def set_mode(self,mode):
        mode = mode.upper()
        if mode == "DATA":
            mode = "J2B"

        command = "MODE,"+mode
        ecc = self.get_ecc(command)
        
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        #print "in set_mode with ", sendStr
        result = self.tx_rx(sendStr)
        if result:
            return result
        else:
            return self.set_mode(mode)
       
        
    def set_rxfreq(self,freq):
        
        fmhz = float(freq) / 1000
        f = str(fmhz)
        
        command = "RXF,"+f
        ecc = self.get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            return result
        else:
            return self.set_rxfreq(freq)
            
            
    def set_txfreq(self,freq):
        
        fmhz = float(freq) / 1000
        f = str(fmhz)
        
        command = "TXF,"+f
        ecc = self.get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            return result
        else:
            return self.set_txfreq(freq)

    def get_txpower():
        command = "TXP"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            list = result.split(",")
            power = list[4].split("*")[0]
            return power
        else:
            return get_txpower()

    def set_txpower(p):
        command = "TXP,"+p
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return set_txpower(p)

    def get_smeter(self):
        command = "SIGM"
        ecc = self.get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = self.tx_rx(sendStr)
        if result:
            list = result.split(",")
            smeter = (float(list[4].split("*")[0]) * 20) - 120 
            return smeter
        else:
            return self.get_smeter()

    def speaker_on():
        command = "SP,ON"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return speaker_on()
        
        
    def speaker_off():
        command = "SP,OFF"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return speaker_off()

    def sql_on():
        command = "SQLC,ON"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return sql_on()

    def sql_off():
        command = "SQLC,OFF"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return sql_off()

    def nb_on():
        command = "NB,ON"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return nb_on()

    def nb_off():
        command = "NB,OFF"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return nb_off()
            
    def dim_on():
        command = "DIM,ON"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return dim_on()

    def dim_off():
        command = "DIM,OFF"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return dim_off()
            
    def agc_on():
        command = "AGC,ON"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return agc_on()

    def agc_off():
        command = "AGC,OFF"
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return agc_off()

    def get_vol():
        command = "AFG"
        ecc = get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            list = result.split(",")
            vol = list[4].split("*")[0]
            return vol
        else:
            return get_vol()
            
            

    def set_vol(v):
        command = "AFG,"+v
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return set_vol(v)

    def get_rfg():
        command = "RFG"
        ecc = get_ecc(command)
        sendStr = preamble+controller+","+radio+","+command+"*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            list = result.split(",")
            rf = list[4].split("*")[0]
            return rf
        else:
            return get_rfg()
            
    def get_att(self):
        return
    def att_on(self):
        return
    def att_off(self):
        return
    
    def pre_on(self):
        return
    def pre_off(self):
        return

    def get_pre(self):
        return

    def set_rfg(v):
        command = "RFG,"+v
        ecc = get_ecc(command)
        sendStr = preamble +controller+","+radio+"," + command + "*"+ecc+cr+lf
        result = tx_rx(sendStr)
        if result:
            return result
        else:
            return set_rfg(v)

    # The message FROM the radio may be corrupted so we do a check on the received ECC versus our calculated cECC
    # from the received characters - which are everything AFTER the "$" and BEFORE the "*"
    #
    # starting the ECC calculation at message[1] ignores the "$" and we iterate through the message XORing each 
    # character's ASCII (decimal) value until we have the final cECC which is converted by formatting it
    # into a two-digit hex value. This is then compared to the received (rECC) value from the radio's message. 
    # If they match the message is acceptable and check_ecc() returns True to tx_rx(), 
    # otherwise check_ecc() function returns "False" to tx_rx()
    # the True/False value is tested in tx_rx(). 
    # If True then tx_rx() returns the incoming string to the calling function
    # otherwise it returns "False". 
    # The calling function then checkS the boolean state of the returned value. 
    # If True (ie it has the radio's message and the ECC was good) the message 
    # is sent back to the client. 
    # If False the function calls itself again, and attempts to get an error-free reply from the radio, via tx_rx()

    def check_ecc(self,message, recc):
        i = 1
        cecc = 0
        
        while i < len(message):
            cecc = ord(message[i]) ^ cecc
            i += 1  
            
        cecc = '{0:02x}'.format(int(cecc))  
        
        if cecc == recc:   
            return True
        else: 
            return False
            
    def tx_rx(self,sendStr):
        #print "in tx_rx, sendStr =  " , sendStr
        lock.acquire()
        
        self.ser.write(sendStr)
        time.sleep(0.1)
        result = self.ser.readline()

        #print result
        reply = result.split("*")
        ecc = reply[1][0:2].lower()
        message = reply[0]
        lock.release()
        
        if self.check_ecc(message, ecc):
            return result
        else:
            return False
        
        
           


#
    
