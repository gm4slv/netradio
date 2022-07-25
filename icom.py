import serial
import threading
from conf import *
import time
#sport = "COM1"
sport = "/dev/ttyS0"
sbaud = 9600

lock = threading.Lock()


class Icom(object):
    def __init__(self, model, radio_address, cal):
        self.ser = serial.Serial(sport, sbaud, timeout=0.1)
        self.model = model
        self.radio_address = radio_address
        self.cal = cal
    
    def digi_off(self):
        sendStr = preamble + preamble + self.radio_address + controller + digi_off_cmd + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"

    def get_pre(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_pre_cmd + eom

        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        if result[6] == "\x00":
            return 0
        elif result[6] == "\x01":
            return 1
        elif result[6] == "\x02":
            return 2

    def get_pwr(self):
        sendStr = preamble + preamble + self.radio_address + controller + pwr_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        p1 = ord(result[7]) / 16
        p2 = ord(result[7]) % 16
        p3 = ord(result[6]) / 16
        p4 = ord(result[6]) % 16
        pwr = float(100 * (10 * p3 + p4) + (10 * p1 + p2))
        return int(pwr*100/255)

    def set_pwr(self, pwr):
        #if pwr == "25":
        #    spwr = "\x00" + "\x63"
        #elif pwr == "50":
        #    spwr = "\x01" + "\x27"
        #elif pwr == "75":
        #    spwr = "\x01" + "\x91"
        #elif pwr == "100":
        #    spwr = "\x02" + "\x55"
        rigpwr = int(pwr) * 255 / 100
        print "rigpwr ", rigpwr
        pwr1 = rigpwr / 100
        pwr2 = rigpwr % 100
        spwr1 = (pwr1 / 10 * 16)
        spwr2 = (pwr1 % 10)
        spwr3 =  (pwr2 / 10 * 16)
        spwr4 =  (pwr2 % 10)
        spwr = chr(spwr1+spwr2) + chr(spwr3+spwr4)
        #print "spwr ", spwr
        sendStr = preamble + preamble + self.radio_address + controller + pwr_cmd + spwr + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return self.get_pwr()
        elif result[4] == nak:
            return "NAK received"

    def pre_on(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_pre_cmd + set_pre_on + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"
    
    def pre_2_on(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_pre_cmd + set_pre_2_on + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"


    def pre_off(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_pre_cmd + set_pre_off + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"

    def ptt_on(self):
        sendStr = preamble + preamble + self.radio_address + controller + ptt_on_cmd + eom
        result = self.tx_rx(sendStr)
        #print result[5]
        if not result[4] == ack:
            return "ptt on"
        elif result[4] == nak:
            return "Error"
    
    def ptt_off(self):
        sendStr = preamble + preamble + self.radio_address + controller + ptt_off_cmd + eom
        result = self.tx_rx(sendStr)
        #print result[5]
        if not result[4] == ack:
            return "ptt off"
        elif result[4] == nak:
            return "Error"

    def get_att(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_att_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        if result[5] == "\x00":
            return 0
        elif result[5] == "\x20":
            return 1

    def att_on(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_att_cmd + set_att_on + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"

    def att_off(self):
        sendStr = preamble + preamble + self.radio_address + controller + set_att_cmd + set_att_off + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Success"
        elif result[4] == nak:
            return "NAK received"

    def set_freq(self, freq):
        fdig = "%010d" % int(freq * 1000)
        bcd = ()
        for i in (8, 6, 4, 2, 0):
            bcd += self.freq_bcd(int(fdig[i]), int(fdig[i + 1]))
        set_freq_val = ""
        for byte in bcd:
            set_freq_val += chr(byte)
        sendStr = preamble + preamble + self.radio_address + controller + set_freq_cmd + set_freq_val + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Set Freq success"
        elif result[4] == nak:
            return "NAK received / Freq not supported"

    def get_freq(self):
        sendStr = preamble + preamble + self.radio_address + controller + get_freq_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        if len(result) > 0:
            f = 0
        for k in [18, 19, 16, 17, 14, 15, 12, 13, 10, 11]:
            f = 10 * f + self.nib(result, k)
        self.freq = (float(f) / 1000)
        return "%.3f" % self.freq

    def set_mode(self, mode):
        print "in set_mode() with ", mode
        if mode == "data":
            mode = "rtty"

        if mode == "lsb":
            set_mode_val = "\x00"
        elif mode == "usb":
            set_mode_val = "\x01"
        elif mode == "am":
            set_mode_val = "\x02"
        elif mode == "cw":
            set_mode_val = "\x03"
        elif mode == "rtty":
            set_mode_val = "\x04"
        elif mode == "fm":
            set_mode_val = "\x05"
        elif mode == "cw-r":
            set_mode_val = "\x07"
        elif mode == "rtty-r":
            set_mode_val = "\x08"
        elif mode == "s-am":
            set_mode_val = "\x11"
        else:
            return "Mode not recognized"
        sendStr = preamble + preamble + self.radio_address + controller + set_mode_cmd + set_mode_val + eom
        result = self.tx_rx(sendStr)
        if result[4] == ack:
            return "Set Mode Success"
        elif result[4] == nak:
            return "NAK received / Mode not supported"

    def get_mode(self):
        sendStr = preamble + preamble + self.radio_address + controller + get_mode_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        mode = ""
        if result[5] == "\x00":
            mode = "lsb"
        elif result[5] == "\x01":
            mode = "usb"
        elif result[5] == "\x02":
            mode = "am"
        elif result[5] == "\x03":
            mode = "cw"
        elif result[5] == "\x04":
            mode = "rtty"
        elif result[5] == "\x05":
            mode = "fm"
        elif result[5] == "\x08":
            mode = "rtty-r"
        elif result[5] == "\x07":
            mode = "cw-r"
        elif result[5] == "\x11":
            mode = "s-am"

        if mode == "rtty":
            mode = "data"

        self.mode = mode
        return self.mode.upper()

    def get_s(self):
        sendStr = preamble + preamble + self.radio_address + controller + get_smeter_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        sm1 = ord(result[7]) / 16
        sm2 = ord(result[7]) % 16
        sm3 = ord(result[6]) / 16
        sm4 = ord(result[6]) % 16
        s = float(100 * (10 * sm3 + sm4) + (10 * sm1 + sm2))
        return s
    
    def get_swr(self):
        sendStr = preamble + preamble + self.radio_address + controller + get_swr_cmd + eom
        result = self.tx_rx(sendStr)
        if not result:
            return "0"
        sm1 = ord(result[7]) / 16
        sm2 = ord(result[7]) % 16
        sm3 = ord(result[6]) / 16
        sm4 = ord(result[6]) % 16
        swr = float(100 * (10 * sm3 + sm4) + (10 * sm1 + sm2))
        return swr

    def get_smeter(self):
        s = float(self.get_s())
        cal = self.cal
        s1 = s - cal[0]
        s2 = s1 - cal[1]
        s3 = s2 - cal[2]
        s4 = s3 - cal[3]
        s5 = s4 - cal[4]
        s6 = s5 - cal[5]
        s7 = s6 - cal[6]
        if s1 <= 0:
            dbm = -123
            adj = s / cal[0] * 10
            return str(dbm + adj)
        elif s2 <= 0:
            dbm = -113
            adj = s1 / cal[1] * 10
            return str(dbm + adj)
        elif s3 <= 0:
            dbm = -103
            adj = s2 / cal[2] * 10
            return str(dbm + adj)
        elif s4 <= 0:
            dbm = -93
            adj = s3 / cal[3] * 10
            return str(dbm + adj)
        elif s5 <= 0:
            dbm = -83
            adj = s4 / cal[4] * 10
            return str(dbm + adj)
        elif s6 <= 0:
            dbm = -73
            adj = s5 / cal[5] * 10
            return str(dbm + adj)
        elif s7 <= 0:
            dbm = -63
            adj = s6 / cal[6] * 20
            return str(dbm + adj)
        else:
            dbm = -43
            adj = s7 / cal[7] * 20
            return str(dbm + adj)

    def get_name(self):
        return self.model

    def tune(self):
        print "tuning"
        curmode = self.get_mode().lower()
        #print "Current Mode ",curmode

        curpwr = self.get_pwr()
        if curpwr < 98:
            curpwr = curpwr + 1

        #print "Current Power ", curpwr
        
        #print "Current percent power ", curpwr
        self.set_mode("rtty")
        self.set_pwr(25)
        #print "Tuning power ", self.get_pwr()
        #print "PTT On"
        self.ptt_on()
        time.sleep(2)
        swr =  self.get_swr()
        #print "SWR :", swr
        time.sleep(1)
        self.ptt_off()
        #print "PTT Off"
        self.set_mode(curmode)
        #print "Mode reset ",self.get_mode()
        self.set_pwr(curpwr)
        print "Tuned : (ref pwr : %s)" % swr
        return "Tuned : (ref pwr : %s)" % swr
        
    def tx_rx(self, sendStr):
        lock.acquire()
        self.ser.write(sendStr)
        echo = self.ser.read(len(sendStr))
        if len(echo) != len(sendStr):
            return "0"
        byte = "0"
        result = ""
        count = 0
        while byte != eom:
            byte = self.ser.read()
            #print "%#02x" % ord(byte)
            result += byte
            count += 1
            if count > 10:
                break
        lock.release()
        #print ""
        return result


    def nib(self, s, i):
        k = ord(s[i / 2])
        if i % 2 == 0:
            k = k >> 4
        return k & 0xf


    def freq_bcd(self, d1, d2):
        return (16 * d1 + d2),

 
