"""
generic handlers for IRC
- automatically joins any channels configured in the session
"""

import logging


class BaseHandler(object):
    def __init__(self, session):
        self.session = session
                
    def process(self, line):
        prefix, command, args = parsemsg(line)
        logging.debug(f'prefix: {prefix}')
        logging.debug(f'command: {command}')
        logging.debug(f'args: {args}')
        if command == '001' and self.session.channels:
            for channel in self.session.channels:
                self.session.send(f'JOIN {channel}')
        elif command == 'PING':
            self.session.pong(args[0])
        elif command == 'PRIVMSG':
            self.handle_message(prefix, command, args)
        elif command == 'NOTICE':
            self.handle_notice(prefix, command, args)
        elif command == 'PART' or command == 'JOIN':
            pass

    def handle_notice(self, prefix, command, args):
        pass

    def handle_message(self, prefix, command, args):
        pass

    def get_nick(self, header):
        return header.split('!')[0].lstrip(':')
    
    
def parsemsg(s):
    """
    Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args
