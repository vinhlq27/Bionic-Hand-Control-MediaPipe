#!pip install serialDevice

import serial
import logging
import serial.tools.list_ports


class SerialObject:
    """
    Allow to transmit data to a serial device like Arduino.
    Example: $01011
    """
    def __init__(self, portNo=None, baudRate=9600, digits=1):
        """
        Initialize the serial object
        :param portNo: Port number.
        :param baudRate: Baud rate.
        :param digits: Number of digits per value to send.
        """
        self.portNo = portNo
        self.baudRate = baudRate
        self.digits = digits

        # Detecting and Connecting a serial device
        connected = False
        if self.portNo is None:
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "Arduino" in p.description:
                    print(f'{p.decription} Connected')
                    self.ser = serial.Serial(p.device)
                    self.ser.baudrate = baudRate
                    connected = True
            if not connected:
                logging.warning("Arduino Not Found. Please enter COM Port Number instead.")

        else:
            try:
                self.ser = serial.Serial(self.portNo, self.baudRate)
                print("Serial Device Connected")
            except:
                logging.warning("Serial Device Not Connected!")

    def sendData(self, data):
        """
        Send data to the serial device.
        :param data: list of values to send.
        """
        myString = "$"      # The string starts with the $ sign
        for d in data:
            myString += str(int(d)).zfill(self.digits)
        try:
            self.ser.write(myString.encode())
            return True
        except:
            return False
