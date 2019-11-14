#!/usr/bin/env python

import serial
import socket
import rospy
from system_monitor.msg import VehicleState

class Controller:
    def __init__(self, **kwargs):
        # Get vehicle name
        self.vehicle_name = socket.gethostname()
        # Get dictionary of peripherals
        self.peripherals = rospy.get_param("asv_description/%s/peripherals" % self.vehicle_name)

        # Set handlers for communication
        for p in self.peripherals:
            if self.peripherals[p]['communication'] == 'serial':
                self.peripherals[p]['_handle'] = serial.Serial(self.peripherals[p]['address'], self.peripherals[p]['baudrate'])
            elif self.peripherals[p]['communication'] == 'tcp':
                self.peripherals[p]['_handle'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.peripherals[p]['_handle'].connect((self.peripherals[p]['address'], self.peripherals[p]['port']))
            elif self.peripherals[p]['communication'] == 'udp':
                self.peripherals[p]['_handle'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Subscribers
        self.status_sub = rospy.Subscriber('/system_monitor/%s/vehicle/state' % self.vehicle_name, VehicleState, callback=self.status_callback)

        # Rate
        self.rate = rospy.Rate(2)   # 2 Hz

        # Messages
        self.vehicle_state = VehicleState()

    def status_callback(self, msg):
        self.vehicle_state = msg

    def run(self):
        # Handle peripherals according to type
        for p in self.peripherals:
            if self.peripherals[p]['type'] == "status_light":
                try:
                    self.peripherals[p]['_handle'].write("%d\n" % self.vehicle_state.id)
                except serial.SerialTimeoutException:
                    rospy.logerr("Timeout writing to serial device in %s" % self.peripherals[p]['address'])

        self.rate.sleep()


if __name__ == "__main__":
    rospy.init_node('asv_control_peripherals', anonymous=True)
    peripherals_control = Controller()
    while not rospy.is_shutdown():
        peripherals_control.run()