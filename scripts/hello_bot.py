

from irc_bot.IRCSession import IRCSession
from irc_bot.HelloHandler import HelloHandler
import logging
from random import randint
import time


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

rando = randint(100, 999)
host = 'irc.dal.net'
port = 6667
nick = f'hellobot{rando}'
ident = nick
realname = nick


session = IRCSession(host, port, nick, ident, realname,
                     channels=['#hello1',
                               '#hello2'],
                     ssl_enabled=False)
handler = HelloHandler(session)
session.connect()
        

while True:
    try:
        lines = session.get_lines()
        for line in lines:
            line = line.rstrip()
            logging.info(line)
            handler.process(line)
    except Exception as e:
        logging.ERROR(f'Exception: {e.args}')
        logging.ERROR(f'Retrying in 5 seconds')
        time.sleep(5)
