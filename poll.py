__author__ = 'gm4slv'

import socket
import os

try:
    import readline
except ImportError:
    pass

import threading
import time


tpoll = 1
HOST, PORT = "snargate", 9999


def make_con():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))


def get_rnum():
    global num
    global radios
    connect("listradios")
    names = receive()

    radios = names.split()
    print radios
    num = len(radios)
    return num


def get_rname(i):
    connect("listradios")
    names = receive()
    radios = names.split()
    r = radios[i]
    return r


def min(smeter_list):
    s = smeter_list
    min = s[0]
    for i in s:
        if i < min:
            min = i
    return min


def max(smeter_list):
    s = smeter_list
    max = s[0]
    for i in s:
        if i > max:
            max = i
    return max


def avg(smeter_list):
    s = smeter_list
    total = 0
    for i in s:
        total = total + i

    average = round((total / len(s)), 1)

    return average


def poll(radio_num, rname):
    print "\n\n"
    # radio = get_rname(i)
    print "radio_num ", radio_num
    print "rname ", rname
    radio = rname
    n = radio_num
    #n = "".join(("r",str(i + 1)))

    smeter_list = []

    while True:
        time.sleep(tpoll)

        try:

            connect("getfreq" + " " + n)
            freq = receive()

            connect("getmode" + " " + str(n))
            mode = receive()

            connect("getsmeter" + " " + str(n))
            dB = receive()

            smeter_list.append(float(dB))

            if len(smeter_list) > 30:
                smeter_list.pop(0)

            average = avg(smeter_list)
            smax = max(smeter_list)
            smin = min(smeter_list)

            os.system('cls' if os.name == 'nt' else 'clear')
            print "-" * 30
            print "{:^30}".format(radio)
            print "-" * 30
            print "Freq:{:>25}".format(freq)
            print "Mode:{:>25}".format(mode)
            print "S-meter:{:>19}dBm".format(dB)

            print "Max/Avg/Min:{:>10}/{:>3}/{:>3}".format(smax, average, smin)
            print "Ave" + "*" * int((113 + average) / 2)
            print "Max" + "|" * int((113 + smax) / 2)
            print "Min" + "|" * int((113 + smin) / 2)
            for i in smeter_list[-30:]:
                print "S  " + "+" * int((113 + i) / 2)

            print "-" * 30



        except:
            print "exception"


def start():
    global radio
    global sock
    print ""
    data = raw_input("Enter \"quit\" at any time to exit\r\n\n").strip()

    if data == "quit":
        connect("quit")
        rx = receive()
        print "Server says: %s " % rx


    else:
        print "Not understood"
        start()


def connect(data):
    global sock
    sock.sendall(data + "\n")


def receive():
    global sock
    received = sock.recv(2048)
    return received


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


make_con()
# get_all()
print "Please choose a radio\r\n"
radio_num, rname = set_radio()
while not radio_num:
    radio_num, rname = set_radio()
print radio_num, rname
t = threading.Thread(target=poll, args=(radio_num, rname))
t.setDaemon(True)
t.start()
start()
