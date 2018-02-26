"""
The main module to hold all the basic GSM
connection functionality and commands
"""

import logging
import sys
import time

import serial

logger = logging.getLogger(__name__)


class GSM(object):
    """
    The base GSM class, inherited by others
    """

    def __init__(self, baud_rate=115200, timeout=2):
        self.baud_rate = baud_rate
        self.port = None
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

            for port in ports:
                try:
                    ser = serial.Serial(port, self.baud_rate, timeout=self.timeout)
                    ser.close()
                    logger.debug('Connected port: ' + port)
                    self.port = port
                    return port
                except:
                    pass

            return None

        else:
            logger.error("non-windows version is not implemented")
            raise NotImplementedError

    def connect(self):
        """
        connect with the serial device
        :return: serial object
        """

        port = self.find_port()
        ser = serial.Serial(port, self.baud_rate, timeout=self.timeout)
        ser.write(b'AT\r\n')
        time.sleep(2)

        response = ser.readlines()
        logger.debug('Response: ' + repr(response))

        check = response[1].decode().strip()
        logger.debug(check)

        if 'OK' in check:
            logger.debug('Serial device connected in port ' + self.port)
            return ser
        return None

    def disconnect(self, ser):
        if ser.is_open == True:
            ser.close()
            logger.debug('Connection closed')

    def listener(self, ser):
        raise NotImplementedError
