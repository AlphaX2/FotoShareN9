
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle

from PySide import QtCore

class FtpPluginSettings(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self._config_path = '/home/user/.config/FotoShareN9/fotoshare_ftp_plugin.cfg'
        self._server = ''
        self._port = ''
        self._path = ''
        self._username = ''
        self._password = ''

    def get_server(self):
        return self._server

    def get_port(self):
        return self._port

    def get_path(self):
        return self._path

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    server = QtCore.Property(unicode, get_server)
    port = QtCore.Property(unicode, get_port)
    path = QtCore.Property(unicode, get_path)
    username = QtCore.Property(unicode, get_username)
    password = QtCore.Property(unicode, get_password)


    @QtCore.Slot()
    def load_settings(self):
        if os.path.isfile(self._config_path):
            print "Found ftp config file - load settings on UI!"
            with open(self._config_path) as f:
                l = pickle.load(f)

                self._server = str(l['server'])
                self._port = str(l['port'])
                self._path = str(l['path'])
                self._username = str(l['username'])
                self._password = str(l['pass'])
        else:
            "Did not find a config file, nothing is loaded on the UI!"


    @QtCore.Slot(str, str, str, str, str)
    def save_settings(self, server, port, path, username, password):

        # load config file or create a new one
        if os.path.isfile(self._config_path):
            print "Found ftp config file - saving new settings!"
            with open(self._config_path) as f:
                l = pickle.load(f)

            l['server'] = str(server)
            l['port'] = str(port)
            l['path'] = str(path)
            l['username'] = str(username)
            l['pass'] = str(password)

            with open(self._config_path, 'w') as f:
                pickle.dump(l,f)
                print "Saved successful ftp-config!"

        else:
            print "Did not found ftp config file, creating new one!"
            with open(self._config_path, 'w') as f:
                pickle.dump(
                            {
                             'server': server,
                             'port': port,
                             'path': path,
                             'username': username,
                             'pass': password,
                             }, f)

            with open(self._config_path) as f:
                l = pickle.load(f)
                print "Saved successful ftp-config!"


    @QtCore.Slot()
    def delete_settings(self):
        """Delete settings file if nothing - all fields are blank"""
        os.remove('/home/user/.config/FotoShareN9/fotoshare_ftp_plugin.cfg')

