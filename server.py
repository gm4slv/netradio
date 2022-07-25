from aor import *
from icom import *
from conf import *
from m710 import *
import SocketServer
import time

try:
    import readline
except:
    pass

lock = threading.Lock()

radios = []



r1 = Icom(n1, a1, cal1)
radios.append(n1)

r2 = m710(n4)
radios.append(n4)

#r2 = Icom(n2, a2, cal2)
#radios.append(n2)

r3 = Ar7030(n3)
radios.append(n3)

print radios
#print r1.digi_off()

#print r2.remote_on()

def count_radios():
    count = len(radios)
    return count


def list_radios():
    radiolist = ""
    for n in range(0, len(radios)):
        r = radios[n]
        radiolist += (r + " ")
    return radiolist


def write_file(text):
    filename = 'commandlog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
    f.write(log)
    f.close()


def write_con(text):
    filename = 'conlog.txt'
    f = open(filename, 'a+')  # a+ is "append to file, create it if it doesn't exist"
    timenow = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time()))
    log = " ".join((timenow, text))  # make an entry for the log by joining the timestamp with the text passed in
    f.write(log)
    f.close()


# The Server
class ThreadedRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        # we find the current thread for the client connection just set up, to
        # use in the log file
        cur_thread = threading.currentThread()
        # log the new connection details
        write_con("Connect from %s using %s \n" % ((self.client_address[0]), cur_thread.getName()))
        # print to the server's console the new connection IP address/port
        print self.client_address
        # loop to handle client requests....
        while True:
            # using StreamRequestHandler means our input from the client
            # is  "file-like" and can be read with "file-like" commands
            # we read a line at a time, using readline()
            cmd = self.rfile.readline().lower()
            # to keep things clean, we remove any characters that aren't
            # "printable" simple ASCII
            # these are between 32 and 127 in the ASCII table
            # we look at each character, and then make a new word by
            # .join()ing each accepted character with no space in between
            asccmd = "".join(x for x in cmd if ord(x) < 128 and ord(x) > 31)
            # we make a list called "words" holding the received words which
            # will be inspected by various functions
            words = asccmd.split()
            # If a client uses sock.close() itself, to disconnect, it appears that
            # we read a continuous stream of "" on the dead
            # socket, which puts CPU to 100%.
            #
            # The "While" loop is probably responsible, but I can't see another
            # way to keep the connection up for multiple commands.
            #
            # Further connection are accepted due to the Threaded nature of the server.
            # The CPU load is unacceptable though
            # HACK ?>>>>>
            # Looking for "" and then breaking
            # the connection from the server end (even though the client has
            # gone) cures this.
            if cmd == "":
                break
            else:
                pass
            # if the words list is empty, go back and get more input
            if not words:
                continue
            # we have input....
            # filter based on the first word - these are the
            # pre-set commands the server will accept
            # the client wants to know the currently available
            # radio names - held in the variable "rnames"
            elif words[0] == "getnames":
                self.wfile.write(rnames)
            # words[-1] (the last word in the list) will always be the
            # radio name. We give the variable "my_radio" this value, for
            # identifying which radio object to apply the method to
            elif words[0] == "count":
                count = count_radios()
                self.wfile.write(count)
            elif words[0] == "ident":
                ident_text = "GM4SLV Radio Server"
                radio_list = list_radios()
                self.wfile.write(ident_text + "\rAvailable : \n" + radio_list + "\r\n")

            elif words[0] == "getmode":
                my_radio = eval(words[-1])
                mode = my_radio.get_mode()
                self.wfile.write(mode)
            elif words[0] == "getfreq":
                my_radio = eval(words[-1])
                freq = words[1]
                freq = my_radio.get_freq()
                self.wfile.write(freq)
            elif words[0] == "setmode":
                my_radio = eval(words[-1])
                mode = words[1]
                newmode = my_radio.set_mode(mode)
                self.wfile.write(newmode)
            elif words[0] == "setfreq":
                my_radio = eval(words[-1])
                try:
                    freq = float(words[1])
                    newfreq = my_radio.set_freq(freq)
                    self.wfile.write(newfreq)
                except ValueError:
                    #freq = float(my_radio.get_freq())
                    self.wfile.write("Error in freq. %s No change\r\n" % words[1])
                    
            elif words[0] == "getsmeter":
                my_radio = eval(words[-1])
                smeter = round(float(my_radio.get_smeter()), 1)
                self.wfile.write(smeter)
            elif words[0] == "gets":
                my_radio = eval(words[-1])
                s = my_radio.get_s()
                self.wfile.write(s)
            elif words[0] == "listradios":
                radios = list_radios()
                self.wfile.write(radios)
            elif words[0] == "getpreamp":
                my_radio = eval(words[-1])
                preamp = my_radio.get_pre()
                self.wfile.write(preamp)
            elif words[0] == "preampon":
                my_radio = eval(words[-1])
                preamp = my_radio.pre_on()
                self.wfile.write(preamp)
            elif words[0] == "preamp2on":
                my_radio = eval(words[-1])
                preamp = my_radio.pre_2_on()
                self.wfile.write(preamp)
            elif words[0] == "preampoff":
                my_radio = eval(words[-1])
                preamp = my_radio.pre_off()
                self.wfile.write(preamp)
            elif words[0] == "getatt":
                my_radio = eval(words[-1])
                att = my_radio.get_att()
                self.wfile.write(att)
            elif words[0] == "atton":
                my_radio = eval(words[-1])
                att = my_radio.att_on()
                self.wfile.write(att)
            elif words[0] == "attoff":
                my_radio = eval(words[-1])
                att = my_radio.att_off()
                self.wfile.write(att)
            elif words[0] == "tune":
                my_radio = eval(words[-1])
                tune = my_radio.tune()
                self.wfile.write(tune)
            elif words[0] == "getpwr":
                my_radio = eval(words[-1])
                pwr = my_radio.get_pwr()
                self.wfile.write(pwr)
            elif words[0] == "setpwr":
                my_radio = eval(words[-1])
                spwr = words[1]
                pwr = my_radio.set_pwr(spwr)
                self.wfile.write(pwr)
            elif words[0] == "quit":
                write_con("Got quit from {}\n".format(self.client_address[0]))  # log it
                self.wfile.write("Goodbye! \r\n")  # say Goodbye
                break
            else:  # nothing in words[0] matches a pre-set command....
                write_file("Received %s\n" % words)  # log it, it's unusual
                self.wfile.write("Command not recognized\r\n")  # inform the client


class ThreadedIcomServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    # define the lock to be used on the serial port access
    lock = threading.Lock()

    # address ('' = all available interfaces) to listen on, and port number
    address = ('', 9999)
    server = ThreadedIcomServer(address, ThreadedRequestHandler)
    server.allow_reuse_address = True

    # define that the server will be threaded, and will serve "forever" ie. not quit after the client disconnects
    t = threading.Thread(target=server.serve_forever)
    # start the server thread
    t.start()

    write_con(
        "Server loop running in thread: %s\n" % "".join(t.getName())) 

