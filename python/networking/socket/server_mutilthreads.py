# -*- coding: utf-8 -*-
#python2.7x
#server_mutilthreads.py
'''
socket服务器的多线程模型
'''

import sys
import socket
import threading
import time

QUIT = False

class ClientThread(threading.Thread):
    def __init__(self, client_sock):
        threading.Thread.__init__(self)
        self.client = client_sock

    def run(self):
        global QUIT
        done = False
        cmd = self.readline()
        while not done:
            if 'quit' == cmd:
                self.writeline("ok, bye")
                QUIT = True
                done = True
            elif 'bye' == cmd:
                self.writeline("ok, bye, bye")
                done = True
            else:
                self.writeline(self.name)

            cmd = self.readline()
        self.client.close()
        return

    def readline(self):
        print  self.client
        result = self.client.recv(200)
        if(None != result):
            result = result.strip().lower()
        return result

    def writeline(self, text):
         self.client.send(text.strip() + '\n')

class Server(object):
    def __init__(self):
        self.sock = None
        self.thread_list = []

    def run(self):
        all_good = False
        try_count = 0

        while not all_good:
            if 3 < try_count:
                sys.exit(1)
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(("0.0.0.0", 8888))
                self.sock.listen(5)
                all_good = True
                break
            except socket.error as err:
                print "socket connection is error, pleace wait 5 scends..."
                del self.sock
                time.sleep(5)
                try_count += 1

        print "server listen on port : 8888"
        print "you can 'telnet localhost 8888' connenct the server"
        print "typing 'quit' close connection"

        try:
            while not QUIT:
                try:
                    self.sock.settimeout(0.50)
                    client = self.sock.accept()[0]
                except socket.timeout:
                    time.sleep(1)
                    if QUIT:
                        print "shutting down"
                        break
                    continue

                new_thread = ClientThread(client)
                print "\nIncoming a connection, started thread.."
                print new_thread.getName()
                self.thread_list.append(new_thread)
                new_thread.start()

                for thread in self.thread_list:
                    if not thread.isAlive():
                        self.thread_list.remove(thread)
                        thread.join()
        except KeyboardInterrupt:
            print "Ctrl+c pressed... shuting down"
        except Exception as e:
            print "some error, %s"%str(e)

            for thread in self.thread_list:
                thread.join(1.0)

            self.sock.close()

if "__main__" == __name__:
        server = Server()
        server.run()
        print "ok"



