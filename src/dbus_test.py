#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop

from PySide import QtCore
from PySide.QtCore import QTimer

class NewFotoCheck:
    def __init__(self):
        print
        print "-== FOTOSHARE N9 DAEMON TEST==-"
        print

#        self.init_dbus()

#    def init_dbus(self):
        #DBUS Init----------------------------------------------------
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        try:
            # Get the remote object
            self.remote_object = self.bus.get_object('com.nokia.maemo.CameraService','/', follow_name_owner_changes=True)
            # Get the remote interface for the remote object
            self.iface = dbus.Interface(self.remote_object, 'com.nokia.maemo.meegotouch.CameraInterface')

            #signal sender=:1.1551 -> dest=(null destination) serial=73 path=/; interface=com.nokia.maemo.meegotouch.CameraInterface; member=cameraClosed


        except dbus.DBusException:
            print_exc()
            sys.exit(1)

        self.iface.connect_to_signal('cameraClosed', self.test_dbus)

    def test_dbus(self, arg1='', arg2=''):
        print "1,2 Test, 1,2 Test"


if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    start = NewFotoCheck()
    sys.exit(app.exec_())

