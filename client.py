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
import time


HOST, PORT = "localhost", 9999

smlog = "pymon.txt"
log_active = []


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
    print ""
    print "The available commands are:"
    print "lr   : List Radios"
    print "sr   : Select the Radio to control"
    print "gr   : Get currently selected Radio name"
    print "gm   : Get Mode"
    print "sm   : Set Mode"
    print "gf   : Get Freq"
    print "sf   : Set Freq"
    print "gs   : Get S-meter"
    print "gp   : Get Pre-amp"
    print "pon  : Set Pre-amp On"
    print "p2on : Set Pre-amp 2 On"
    print "poff : Set Pre-amp Off"
    print "gatt : Get Attn"
    print "aton : Set Attn On"
    print "atoff: Set Attn Off"
    print "ga   : Get All (status of all radios)"
    print "sync : Sync freq/mode on two radios"
    print "log  : Setup background logging to file"
    print "h    : Help (show this command list)"
    print "q    : quit"
    print ""


def start():
    global radio_num
    global rname
    global sock
    pfreq = connect("getfreq" + " " + radio_num)
    pmode = connect("getmode" + " " + radio_num)
    
    data = raw_input(rname + " (" + pfreq + " " + pmode + ") " + " > ").lower().strip()
    if len(data.split()) > 1:
        if (data.split())[0] == "sf":
            sfreq = (data.split())[1]
            freq = connect("setfreq" + " " + sfreq + " " + radio_num)
            print "%s replied: %s" % (rname, freq)
            start()
        elif (data.split())[0] == "sm":
            smode = (data.split())[1]
            mode = connect("setmode" + " " + smode + " " + radio_num)
            print "%s replied: %s" % (rname, mode)
            start()
        else:
            
            print "only one command at a time please"
            start()
    elif data == "u":
        oldf = connect("getfreq" + " " + radio_num)
        newf = str(float(oldf) + 1)
        freq = connect("setfreq" + " " + newf + " " + radio_num)
        print "%s replied: %s" % (rname, freq)
        start()
    
    elif data == "d":
        oldf = connect("getfreq" + " " + radio_num)
        newf = str(float(oldf) - 1)
        freq = connect("setfreq" + " " + newf + " " + radio_num)
        print "%s replied: %s" % (rname, freq)
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
        smode = raw_input("Enter mode: ")
        mode = connect("setmode" + " " + smode + " " + radio_num)
        print "%s replied: %s" % (rname, mode)
        start()

    elif data == "gf":
        freq = connect("getfreq" + " " + radio_num)
        print "%s replied: %s kHz" % (rname, freq)
        start()

    elif data == "sf":
        sfreq = raw_input("Enter freq (kHz): ")
        freq = connect("setfreq" + " " + sfreq + " " + radio_num)
        print "%s replied: %s" % (rname, freq)
        start()

    elif data == "gs":
        smeter = connect("getsmeter" + " " + radio_num)
        print "%s replied: %sdBm" % (rname, smeter)
        start()

    elif data == "gp":
        preamp = connect("getpreamp" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "pon":
        preamp = connect("preampon" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()
    
    elif data == "p2on":
        preamp = connect("preamp2on" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "poff":
        preamp = connect("preampoff" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "gatt":
        preamp = connect("getatt" + " " + radio_num)
        print "%s replied: %s" % (rname, preamp)
        start()

    elif data == "aton":
        att = connect("atton" + " " + radio_num)
        print "%s replied: %s" % (rname, att)
        start()

    elif data == "atoff":
        att = connect("attoff" + " " + radio_num)
        print "%s replied: %s" % (rname, att)
        start()

    elif data == "ga":
        get_all()
        start()


    elif data == "log":
        fname = raw_input("Enter a filename (or \"Return\" for default) :")
        if fname == "":
            fname = smlog
        # check file is valid
        try:
            f = open(fname, 'a+')
            f.close()
        except IOError:
            print "File/path not valid"
            start()

        list_radios()

        lradio = get_lradio()

        while not lradio:
            lradio = get_lradio()

        rname = get_rname(int(lradio) - 1)
        if lradio in log_active:
            print "Logging already active on " + rname
        else:
            tlog = int(raw_input("Enter a polling interval (seconds) :"))
            p = threading.Thread(target=log, args=(lradio, tlog, fname))
            p.setDaemon(True)
            p.start()
            log_active.append(lradio)
        start()

    elif data == "sync":
        sync_result = sync()
        print sync_result
        start()


    elif data == "h" or data == "help":
        prompt()
        start()


    elif data == "q" or data == "quit":
        rx = connect("quit")
        print "Server says: %s " % rx

    else:
        #prompt()
        start()


def get_all():
    num = get_rnum()
    global radio
    print "There are currently %d radios connected." % num
    print "=" * 33
    for i in range(0, num):
        r = get_rname(i)
        n = "".join(("r", str(i + 1)))
        freq = connect("getfreq" + " " + n)
        mode = connect("getmode" + " " + str(n))
        smeter = connect("getsmeter" + " " + str(n))
        preamp = connect("getpreamp" + " " + str(n))
        att = connect("getatt" + " " + str(n))

        print "Status of Radio %d (%s) \r\n" % (i + 1, r)
        print "Frequency : %s kHz" % freq
        print "Mode: %s" % mode
        print "S-Meter: %sdBm" % smeter
        print "Preamp = %s" % preamp
        print "Attenuator = %s " % att
        print "=" * 33

    print ""


def log(p, t, f):
    print "\n\n"
    tlog = t
    sradio = get_rname(int(p) - 1)

    sr = "".join(("r", str(p)))
    while True:
        try:
            frequency = connect("getfreq" + " " + sr + "\n")
            smeter = connect("getsmeter" + " " + sr + "\n")
            mode = connect("getmode" + " " + sr + "\n")
            write_file(f, sradio, mode, frequency, smeter)
            time.sleep(tlog)
        finally:
            pass


def get_mradio():
    num = get_rnum()

    mradio = raw_input("Choose Master radio number from the list: ").strip()

    if not mradio:
        print "Please select a radio"
        return False
    elif int(mradio) > num:
        print "Selected radio not recognized"
        return False

    else:

        return mradio


def get_sradio():
    num = get_rnum()
    sradio = raw_input("Choose Slave radio number from the list: ").strip()

    if not sradio:
        print "Please select a radio"
        return False
    elif int(sradio) > num:
        print "Selected radio not recognized"
        return False

    else:

        return sradio


def sync():
    num = get_rnum()
    print ""
    print "Set SLAVE to the same Frequency and Mode as MASTER.\r\n"
    print "Currently connected radios are:"
    for i in range(0, num):
        r = get_rname(i)
        print "%d is %s" % (i + 1, r)

    mradio = get_mradio()
    while not mradio:
        mradio = get_mradio()

    sradio = get_sradio()
    while not sradio:
        sradio = get_sradio()
    sr = "".join(("r", sradio))
    mr = "".join(("r", mradio))
    mfreq = connect("getfreq" + " " + mr)
    mmode = connect("getmode" + " " + mr)

    sfreq = connect("setfreq" + " " + mfreq + " " + sr)
    smode = connect("setmode" + " " + mmode + " " + sr)

    return (sfreq + "\r\n" + smode + "\r\n")


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
print "Please choose a radio\r\n"
radio_num, rname = set_radio()
while not radio_num:
    radio_num, rname = set_radio()

prompt()
start()
