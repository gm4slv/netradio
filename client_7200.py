__author__ = 'gm4slv'
# client to work with server_oo.py
# 

# # v0.1

import socket

try:
    import readline
except ImportError:
    pass

import threading

HOST, PORT = "localhost", 9999

def make_con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))


def get_rnum():
    global num
    global radios

    names = connect("listradios")

    radios = names.split()
    num = len(radios)
    return num


def get_rname(i):
    r = radios[i]
    return r


def list_radios():
    num = get_rnum()
    global radio
    print "\r\nThere are currently %d radios connected." % num
    for i in range(0, num):
        r = get_rname(i)
        print "Radio %d is %s" % (i + 1, r)


def get_lradio():
    num = get_rnum()

    lradio = raw_input("Select radio to log: ").strip()

    if not lradio:
        print "Please select a radio"
        return False
    elif int(lradio) > num:
        print "Selected radio not recognized"
        return False

    else:

        return lradio


def set_radio():
    num = get_rnum()
    # global radio
    global radio_num
    global rname
    print "There are currently %d radios connected." % num
    for i in range(0, num):
        r = get_rname(i)
        print "Radio %d is %s" % (i + 1, r)

    radio = raw_input("Choose a radio number from the list : ").strip()
    try:
        if not radio:
            print "Please select a radio"
            return False, False

        elif int(radio) > num:
            print "Selected radio not recognized"
            return False, False
    except ValueError:
        print "Please enter a number"
        return False, False

    else:
        radio_num = "".join(("r", radio))
        rname = get_rname(int(radio) - 1)
        return radio_num, rname


def prompt():
    print "=" * 40
    print "gm   : Get Mode      sm   : Set Mode"
    print "gf   : Get Freq      sf   : Set Freq"
    print "gs   : Get S-meter"
    print "=" * 40
    print "gp   : Get Pre-amp"
    print "pon  : Pre-amp On    poff : Pre-amp Off"
    print "gatt : Get Attn"
    print "aton : Attn On       atoff: Attn Off"
    print "=" * 40
    print "gpwr : Get TX pwr    spwr : Set TX pwr"
    print "tune : 3 second ATU Tune"
    print "ga   : Get All"
    print "=" * 40
    print "h    : Help (show this command list)"
    print "q    : quit"
    print ""


def start():
    global radio_num
    global rname
    global sock

    data = raw_input(rname + " > ").lower().strip()
    if len(data.split()) > 1:
        print "only one command at a time please"
        start()

    elif data == "lr":
        list_radios()
        start()
    elif data == "sr":

        radio_num, rname = set_radio()

        while not radio_num:
            radio_num, rname = set_radio()

        start()

    elif data == "gr":
        print "Radio selected is %s" % rname
        start()

    elif data == "gm":
        mode = connect("getmode" + " " + radio_num)
        print "%s replied: %s" % (rname, mode)
        start()

    elif data == "sm":
        smode = raw_input("Enter mode: ").lower()
        if smode == "u":
            smode = "usb"
        elif smode == "l":
            smode = "lsb"
        elif smode == "a":
            smode = "am"
        elif smode == "c":
            smode = "cw"
        elif smode == "r":
            smode = "rtty"
        mode = connect("setmode" + " " + smode + " " + radio_num)
        print "%s replied: %s" % (rname, mode)
        start()

    elif data == "gf":
        freq = connect("getfreq" + " " + radio_num)
        print "%s replied: %s kHz" % (rname, freq)
        start()
        
    elif data == "sf":
        sfreq = raw_input("Enter freq (kHz): ")
        try:
            f = float(sfreq)
        except:
            print "Freq. not recognized"
            start()
        freq = connect("setfreq" + " " + sfreq + " " + radio_num)
        print "%s replied: %s" % (rname, freq)
        start()




    elif data == "gs":
        smeter = connect("getsmeter" + " " + radio_num)
        print "%s replied: %sdBm" % (rname, smeter)
        start()
        
    elif data == "gpwr":
        pwr = connect("getpwr" + " " + radio_num)
        print "%s replied: %s" % (rname, pwr)
        start()
    
    elif data == "spwr":
        spwr = raw_input("Enter percent [0-100] ")
        try:
            p = float(spwr)
        except:
            print "Power not recognized"
            start()
        pwr = connect("setpwr" + " " + spwr + " " + radio_num)
        print "%s replied: %s" % (rname, pwr)
        start()
    
        
    elif data == "gp":
        preamp = connect("getpreamp" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "pon":
        preamp = connect("preampon" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        get_all()
        start()

    elif data == "poff":
        preamp = connect("preampoff" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        get_all()
        start()

    elif data == "gatt":
        preamp = connect("getatt" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "aton":
        att = connect("atton" + " " + radio_num)
        print "%s replied: %s" % (rname, att)
        get_all()
        start()

    elif data == "atoff":
        att = connect("attoff" + " " + radio_num)
        print "%s replied: %s" % (rname, att)
        get_all()
        start()
        
    elif data == "tune" or data == "t":
        tune = connect("tune" + " " + radio_num)
        print "%s replied: %s" % (rname, tune)
        start()

    elif data == "ga":
        get_all()
        start()

        
    elif data == "h" or data == "help":
        prompt()
        start()


    elif data == "q" or data == "quit":
        rx = connect("quit")
        print "Server says: %s " % rx

    else:
        prompt()
        start()


def get_all():
    num = get_rnum()
    global radio
    #print "There are currently %d radios connected." % num
    print "-" * 46
    for i in range(0, num):
        r = get_rname(i)
        n = "".join(("r", str(i + 1)))
        freq = connect("getfreq" + " " + n)
        mode = connect("getmode" + " " + str(n))
        smeter = connect("getsmeter" + " " + str(n))
        preamp = connect("getpreamp" + " " + str(n))
        att = connect("getatt" + " " + str(n))
        if preamp == "1":
            preamp = "On"
        else:
            preamp = "Off"
        if att == "1":
            att = "On"
        else:
            att = "Off"
            
        #print "Status of Radio %d (%s) \r\n" % (i + 1, r)
        print "Frequency : %s kHz,  Mode : %s" % (freq, mode)
        print "RSL : %sdBm,  Preamp : %s,  Att : %s" % (smeter, preamp, att)
        print "-" * 46



# Try to send and receive in one-go, to prevent the logging thread and the main prog
# getting the wrong receive data

def connect(data):
    try:
        lock.acquire()
        global sock
        sock.sendall(data + "\n")
        received = sock.recv(2048)
    finally:
        lock.release()

    return received


def write_file(fname, rname, mode, freq, smeter):
    filename = fname
    f = open(filename, 'a+')
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, rname, mode, freq, smeter, "\r\n"))
    f.write(log)
    f.close()


make_con()

lock = threading.Lock()
get_all()
#print "Please choose a radio\r\n"
#radio_num, rname = set_radio()
#while not radio_num:
#    radio_num, rname = set_radio()
radio_num = "r1"
rname = "IC-7200"
prompt()
start()
