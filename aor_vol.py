import serial
import threading


#sport = "/dev/ttyS0"
sport = "/dev/ttyUSB1"
sbaud = 1200

lock = threading.Lock()
fract = float(2 ** 24) / 44545


class Ar7030(object):
    def __init__(self, model):
        self.ser = serial.Serial(sport, sbaud, timeout=10)
        self.model = model
        self.af = self.af_on()
        self.mute = self.mute_af_2()



    def check_bit(self, byte, bit):
        mask = 1 << bit
        result = (ord(byte) & mask)
        if result:
            return 1
        else:
            return 0

    def set_bit(self, byte, bit):
        mask = 1 << bit
        result = ord(byte) | mask
        return result

    def clear_bit(self, byte, bit):
        mask = ~(1 << bit)
        result = (ord(byte) & mask)
        return result

    def get_ident(self):
        sendStr = '\x5f' + '\x40'
        ident = self.tx_rx(sendStr, False, 8)
        return ident

    def get_pre(self):
        sendStr = '\x50' + '\x32' + '\x48'
        byte = self.tx_rx(sendStr, False, 1)
        p = self.check_bit(byte, 4)
        if p:
            return 1
        else:
            return 0
        return


    def pre_on(self):
        #get current 8-bit rxcon byte :
        # bit0 = filter FS3
        # bit1 = filter FS2
        # bit2 = filter FS1
        # bit3 = filter FS4
        # bit4 = preamp enabled
        # bit5 = atten 0 = 20dB / 1 = 40dB
        # bit6 = input filter 0 = HF / 1 = LF
        # bit7 = attenuator enabled

        sendStr = '\x50' + '\x32' + '\x48'

        byte = self.tx_rx(sendStr, False, 1)

        # set bit 4 ON = preamp ON and get the new 8-bit rxcon byte
        pon = self.set_bit(byte, 4)

        # split new rxcon byte into two 4-bit nibbles, add 48/96 (\x30 and \x60)
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)

        sendStr = '\x81' + '\x50' + '\x32' + '\x48' + chr(high) + chr(low) + '\x29' + '\x80'

        self.tx_rx(sendStr, False, 0)

        return "Command sent"


    def pre_off(self):
        #get current 8-bit rxcon byte
        sendStr = '\x50' + '\x32' + '\x48'
        byte = self.tx_rx(sendStr, False, 1)

        # set bit 4 OFF = preamp OFF and get the new 8-bit rxcon byte
        pon = self.clear_bit(byte, 4)


        # split new rxcon byte into two 4-bit nibbles, add 48/96 (\x30 and \x60)
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)

        sendStr = '\x81' + '\x50' + '\x32' + '\x48' + chr(high) + chr(low) + '\x29' + '\x80'

        self.tx_rx(sendStr, False, 0)
        return "Command sent"


    def get_att(self):
        sendStr = '\x50' + '\x32' + '\x48'

        byte = self.tx_rx(sendStr, False, 1)

        a = self.check_bit(byte, 7)

        if a:
            return 1
        else:
            return 0

    def mute_af(self):
        sendStr = '\x50' + '\x31' + '\x4E'
        byte = self.tx_rx(sendStr, False, 1)
        print ord(byte)
        high = 48
        low = 96 + 15
        sendStr = '\x81' + '\x50' + '\x31' + '\x4E' + chr(high) + chr(low) + '\x25' + '\x80'
        self.tx_rx(sendStr, False, 0)
        return "Command Sent"
    
    def mute_af_2(self):
        sendStr = '\x50' + '\x32' + '\x47'
        byte = self.tx_rx(sendStr, False, 1)
        print ord(byte)
        pon = self.set_bit(byte,6)
        print pon
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)
        
        sendStr = '\x81' + '\x50' + '\x32' + '\x47' + chr(high) + chr(low) + '\x25' + '\x80'
        self.tx_rx(sendStr, False, 0)
        #self.af_on()
        return "Command Sent"

    def af_on(self):
        sendStr = '\x50' + '\x31' + '\x4E'
        byte = self.tx_rx(sendStr, False, 1)
        print ord(byte)
        pon = self.clear_bit(byte,4)
        print pon
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)
        sendStr = '\x81' + '\x50' + '\x31' + '\x4E' + chr(high) + chr(low) + '\x25' + '\x80'
        self.tx_rx(sendStr, False, 0)
        return "Command Sent"

    def att_on(self):
        #get current 8-bit rxcon byte
        sendStr = '\x50' + '\x32' + '\x48'
        byte = self.tx_rx(sendStr, False, 1)
        print "Byte ", ord(byte)

        # set bit 7 ON = ATT ON and get the new 8-bit rxcon byte
        pon = self.set_bit(byte, 7)


        # split new rxcon byte into two 4-bit nibbles, add 48/96 (\x30 and \x60)
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)
        print "high ", high
        print "low ", low

        sendStr = '\x81' + '\x50' + '\x32' + '\x48' + chr(high) + chr(low) + '\x29' + '\x80'

        self.tx_rx(sendStr, False, 0)
        return "Command sent"


    def att_off(self):
        #get current 8-bit rxcon byte
        sendStr = '\x50' + '\x32' + '\x48'
        byte = self.tx_rx(sendStr, False, 1)
        print "Byte ", ord(byte)

        # set bit 7 OFF = att OFF and get the new 8-bit rxcon byte
        pon = self.clear_bit(byte, 7)


        # split new rxcon byte into two 4-bit nibbles, add 48/96 (\x30 and \x60)
        high = 48 + (pon >> 4)
        low = 96 + (pon & 15)
        print "high ", high
        print "low ", low

        sendStr = '\x81' + '\x50' + '\x32' + '\x48' + chr(high) + chr(low) + '\x29' + '\x80'

        self.tx_rx(sendStr, False, 0)
        return "Command sent"


    def set_freq(self, freq):
        fval = freq * fract
        #print fval
        b1 = 48 + int(fval / 1048576)
        fval = fval % 1048576
        b2 = 96 + int(fval / 65536)
        fval = fval % 65536
        b3 = 48 + int(fval / 4096)
        fval = fval % 4096
        b4 = 96 + int(fval / 256)
        fval = fval % 256
        b5 = 48 + int(fval / 16)
        b6 = 96 + int(fval % 16)

        f_tuple = ( b1, b2, b3, b4, b5, b6 )

        freqStr = ""
        for byte in f_tuple:
            freqStr += chr(byte)

        sendStr = '\x81' + '\x50' + '\x31' + '\x4a' + freqStr + '\x24' + '\x80'

        self.tx_rx(sendStr, False, 0)
        return "Freq Set"

    def get_freq(self):

        sendStr = '\x50' + '\x31' + '\x4a'

        freqStr = self.tx_rx(sendStr, False, 3)

        f_val = 0
        for k in freqStr:
            f_val = f_val * 256 + ord(k)

        return "%.3f" % round(float(f_val / fract),2 )
        


    def set_mode(self, mode):

        if mode == "lsb":
            set_mode_val = "\x66"
        elif mode == "usb":
            set_mode_val = "\x67"
        elif mode == "am":
            set_mode_val = "\x61"
        elif mode == "cw":
            set_mode_val = "\x65"
        elif mode == "data":
            set_mode_val = "\x64"
        elif mode == "fm":
            set_mode_val = "\x63"
        elif mode == "s-am":
            set_mode_val = "\x62"
        else:
            return "Mode not recognized"

        sendStr = '\x81' + '\x50' + '\x31' + '\x4d' + set_mode_val + '\x22' + '\x80'

        self.tx_rx(sendStr, False, 0)

        return "Mode sent"

    def get_mode(self):

        sendStr = "\x50" + "\x31" + "\x4d"
        m = self.tx_rx(sendStr, False, 1)

        mode = ""
        if m == "\x01":
            mode = "am"
        elif m == "\x02":
            mode = "s-am"
        elif m == "\x03":
            mode = "fm"
        elif m == "\x04":
            mode = "data"
        elif m == "\x05":
            mode = "cw"
        elif m == "\x06":
            mode = "lsb"
        elif m == "\x07":
            mode = "usb"

        return mode.upper()


    def get_s(self):
        sendStr = '\x2e'
        sraw = self.tx_rx(sendStr, True, 0)

        return ord(sraw)

    def get_cal(self):

        sendStr = '\x52' + '\x3f' + '\x44' + '\x11'
        #print "sending getcal"
        cbytes = self.tx_rx(sendStr, False, 8)

        cal = []

        for c in cbytes:
            cal.append(ord(c))

        return cal

    def get_smeter(self):
        s = float(self.get_s())
        cal = self.get_cal()

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


    def tx_rx(self, sendStr, reply, n):
        # apply thread lock
        lock.acquire()
        self.ser.write(sendStr)

        if reply:  # for reading S-meter
            result = ""
            while not result:
                result = self.ser.read(1)
            lock.release()
            return result
        else:

            result = ""
            byte = ""
            while n != 0:
                self.ser.write('\x71')
                #byte = ""

                while not byte:
                    byte = self.ser.read(1)

                result += byte

                byte = ""
                n -= 1
            lock.release()
            return result



