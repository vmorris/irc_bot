"""
Generic IRC Session
- connects to an IRC server and handles sending and receiving data
- call connect() manually, login is automatic
- SSL can be optionally enabled and SSL verification is off by default
"""

import socket
import ssl


class IRCSession():
    def __init__(self, host, port, nick, ident, realname,
                 nickserv_password=None,
                 channels=None,
                 ssl_enabled=False, ssl_verify=False):
        self.host = host
        self.port = port
        self.nick = nick
        self.ident = ident
        self.realname = realname
        self.nickserv_password = nickserv_password
        self.channels = channels
        self.ssl_enabled = ssl_enabled
        self.ssl_verify = ssl_verify
        self.sock = None
        self.recv_buffer = ''

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))
        if self.ssl_enabled:
            context = ssl.create_default_context()
            if not self.ssl_verify:
                # disable hostname checking
                context.check_hostname = False
                # disable certificate verification
                context.verify_mode = ssl.CERT_NONE
            self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
        self._login()

    def get_lines(self):
        # append data to buffer
        self.recv_buffer += self._get_data()
        # split all data in buffer on newline
        lines = self.recv_buffer.split('\n')
        # the last line entry may not be complete (no newline)
        # clear the buffer and pop the last line back
        self.recv_buffer = lines.pop()
        return lines

    def send(self, msg):
        to_send = f'{msg}\r\n'.encode()
        self.sock.sendall(to_send)

    def get_nick(self):
        return self.nick

    def get_ident(self):
        return self.ident

    def _login(self):
        self.send(f'NICK {self.nick}')
        self.send(f'USER {self.ident} {self.host} greetz :{self.realname}')

    def _get_data(self):
        return self.sock.recv(1024).decode()
    