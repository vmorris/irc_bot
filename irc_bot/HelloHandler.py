"""
Message Handler for Hello World
"""

from irc_bot.BaseHandler import BaseHandler


class HelloHandler(BaseHandler):
    def __init__(self, session):
        super().__init__(session)
    
    def handle_notice(self, prefix, command, args):
        pass

    def handle_message(self, prefix, command, args):
        sender = self.get_nick(prefix)
        channel = args[0]
        message = args[1]
        if sender == self.session.nick:
            # ignore messages from ourself
            return
        elif channel == self.session.nick:
            # somebody sent us a direct message
            self._handle_private_message(sender, message)
        elif channel.startswith('#'):
            # somebody sent a message in a channel
            self._handle_channel_message(channel, message)

    def _handle_private_message(self, sender, message):
        self.session.send_message(sender, 'hi {sender}!')
    
    def _handle_channel_message(self, channel, message):
        if message.startswith(f'@{self.session.nick} help'):
            self._send_help(channel)
        if message.startswith(f'@{self.session.nick} echo'):
            to_echo = message.split('echo ', 1)[1]
            if len(to_echo) == 0:
                self.session.send_message(channel, 'What do you want me to echo?')
            else:
                self.session.send_message(channel, to_echo)
            
    def _send_help(self, channel):
        self.session.send_message(channel, 'Hello there, I am a dumb bot!')
        self.session.send_message(channel, f'Prefix commands with @{self.session.nick}')
        self.session.send_message(channel, 'commands:')
        self.session.send_message(channel, ' help')
        self.session.send_message(channel, ' echo')
