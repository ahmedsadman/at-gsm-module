"""
The main module to hold all the basic GSM
connection functionality and commands
"""

import logging
import sys
import time
import serial
import glob
from threading import Thread

logger = logging.getLogger(__name__)


class GSM(object):
    """
    The base GSM class
    """

    # borg pattern
    _shared = {}

    port = None
    conn = None

    def __init__(self, baud_rate=115200, timeout=2):
        self.__dict__ = self._shared
        self.baud_rate = baud_rate
        self.timeout = timeout

    def find_port(self):
        """
        find the working port connected with the serial
        communication device
        :return: port number -> string
        """

        logger.debug('Searching for ports...')

        # for windows os
        if 'win' in sys.platform:
            ports = ['COM%s' % (i + 1) for i in range(255)]
        elif 'linux' in sys.platform:
            ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        else:
            logger.critical('Your OS is not supported')
            ports = []

        for port in ports:
            try:
                ser = serial.Serial(port, self.baud_rate, timeout=self.timeout)
                ser.close()
                logger.debug('Connected port: ' + port)
                self.port = port
                return port
            except serial.serialutil.SerialException:
                pass

        logger.error('No port found')
        return None

    def connect(self):
        """
        connect with the serial device
        :return: serial object
        """

        port = self.find_port()
        logger.debug('Establishing connection...')
        ser = serial.Serial(port, self.baud_rate, timeout=self.timeout)
        ser.write(b'AT\r\n')

        response = ser.readlines()
        logger.debug('Response: ' + repr(response))

        check = response[1].decode().strip()
        logger.debug(check)

        if 'OK' in check:
            logger.debug('Serial device connected in port ' + self.port)
            self.conn = ser
            self.start_listener()
            return ser
        return None

    def disconnect(self):
        if self.conn.is_open:
            self.conn.close()
            logger.debug('Connection closed')

    def listener(self):
        """
        A listener to read serial device response, should
        be run in a thread
        :return: None
        """

        if not self.conn.is_open:
            logger.error('Serial device not connected')

        while self.conn.is_open:
            if self.conn.inWaiting() > 0:
                response = self.conn.readlines()
                logger.debug('Listener: ' + repr(response))
            time.sleep(1)

    def start_listener(self):
        logger.debug('Starting non-blocking listener')
        t = Thread(target=self.listener)
        t.start()
        logger.debug('Listening...')

    def send(self, command):
        """
        send a command to the serial device
        :param command: string
        :return: None
        """

        command += '\r\n'
        logger.debug('Sending command: ' + command)
        command = command.encode()
        self.conn.write(command)
