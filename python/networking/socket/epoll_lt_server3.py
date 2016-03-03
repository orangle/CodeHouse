# -*- coding: utf-8 -*-
"""
采用对象化的组织方式
ref:https://gist.github.com/kykyev/3136452
Simple tcp server for educational purposes.
Based directly on python interface to Linux epoll mechanism.
Uses vanilla plain callback style.
"""

import socket
import select
import errno
from functools import partial

TERM = '\n'
EOL1 = '\n\n'
EOL2 = '\n\r\n'

def init_server_socket(host='0.0.0.0', port=9999):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.setblocking(0)
    ss.bind((host, port))
    ss.listen(100)
    return ss

class Stream(object):
    """Instances of `Stream` class represent io-state on a socket.

    conn:
        connection object
    req:
        stream of bytes to be read
    resp:
        stream of bytes to be written
    """
    def __init__(self, conn, req='', resp=''):
        self.conn = conn
        self.req = req
        self.resp = resp


class Server(object):
    """Simple tcp server.
    def application(request, write_response):
        write_response(">>> {}:{}\n".format(request, len(request)))
    server = Server(app=application)
    server.start()
    """
    def __init__(self, app):
        self.server_socket = init_server_socket()
        self.epoll = select.epoll()
        self.state = {}
        self.app = app
        self.epoll.register(self.server_socket.fileno(), select.EPOLLIN)

    def _handle_accept(self):
        """ """
        conn, addr = self.server_socket.accept()
        conn.setblocking(0)
        print "opening connection, fileno: {0} ".format(conn.fileno())
        self.epoll.register(conn.fileno(), select.EPOLLIN)
        self.state[conn.fileno()] = Stream(conn)

    def _handle_read(self, fileno):
        """ """
        s = self.state[fileno]
        s.req += s.conn.recv(1024)
        terminal_index = s.req.find(TERM)
        if terminal_index:
            req_ready = s.req[:terminal_index]
            s.req = s.req[terminal_index + 1:]
            self.app(req_ready, partial(self._write_response, fileno))

    def _handle_write(self, fileno):
        """ """
        s = self.state[fileno]
        try:
            bytes_written = s.conn.send(s.resp)
        except socket.error as e:
            # in case when peer has closed connection
            if e.errno == errno.EPIPE:
                self._close_connection(fileno)
            else:
                raise e
        else:
            s.resp = s.resp[bytes_written:]
            if not s.resp:
                self.epoll.modify(fileno, select.EPOLLIN)

    def _handle_hup(self, fileno):
        """ """
        self._close_connection(fileno)

    def _loop(self):
        try:
            while True:
                events = self.epoll.poll(1)
                for fileno, evt in events:
                    if fileno == self.server_socket.fileno():
                        self._handle_accept()
                    # It important that EPOLLHUP goes before EPOLLIN.
                    # Otherwise _handle_hup is never reached because
                    # EPOLLHUP occures not alone but in conjunction
                    # with EPOLLIN or EPOLLOUT.
                    elif evt & select.EPOLLHUP:
                        self._handle_hup(fileno)
                    elif evt & select.EPOLLIN:
                        self._handle_read(fileno)
                    elif evt & select.EPOLLOUT:
                        self._handle_write(fileno)
        finally:
            self.shutdown()

    def _close_connection(self, fileno):
        print "closing connection, fileno: {0} ".format(fileno)
        self.epoll.unregister(fileno)
        self.state[fileno].conn.close()
        del self.state[fileno]

    def _write_response(self, fileno, response):
        self.state[fileno].resp = response
        self.epoll.modify(fileno, select.EPOLLOUT)

    def start(self):
        self._loop()

    def shutdown(self):
        self.epoll.unregister(self.server_socket.fileno())
        self.epoll.close()
        self.server_socket.close()


if __name__ == "__main__":
    response = "HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 2016 18:05:30 GMT\r\n"
    response += "Content-Type: text/palin\r\nContent-Length: 13\r\n\r\n"
    response += "Hello, world\n"
    def application(request, write_response):
        write_response(response)

    server = Server(app=application)
    server.start()
