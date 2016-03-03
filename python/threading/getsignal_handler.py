#coding:utf-8
#orangleliu py2.7
#getsignal_handler.py

import signal

def handle_hup(sig, frame):
    print "get signal: %s"%sig

signal.signal(1, handle_hup)

if __name__ == "__main__":

    ign = signal.SIG_IGN
    dfl = signal.SIG_DFL
    print "SIG_IGN", ign
    print "SIG_DFL", dfl
    print "*"*40

    for name in dir(signal):
        if name[:3] == "SIG" and name[3] != "_":
            signum = getattr(signal, name)
            gsig = signal.getsignal(signum)

            print name, signum, gsig



