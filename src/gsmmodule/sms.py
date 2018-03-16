import time
import logging
from gsmmodule import GSM

logger = logging.getLogger(__name__)


class SMS(object):
    """
    SMS handler class
    """

    def __init__(self):
        self.gsm = GSM()
        self.gsm.connect()
        self.gsm.send('AT+CMGF=1')
        logger.debug('SMS module initiated')

    def send_sms(self, recipient, text):
        self.gsm.send('AT+CMGS="' + recipient + '"')
        time.sleep(2)
        self.gsm.send(text.strip())
        time.sleep(2)
        self.gsm.conn.write(bytes([26]))
        logger.debug('SMS sent')