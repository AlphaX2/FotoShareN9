
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle

import paramiko


class SftpUploadPlugin:
    def __init__(self):
        self.config_path = '/home/user/.config/FotoShareN9/fotoshare_sftp_plugin.cfg'

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            # normal settings
            self.server_adress = l['server']
            self.server_port = l['port']
            self.server_folder = l['path'] 
            self.server_user = l['username']
            self.server_pass = l['pass']

            self.hostkey = None

            f.close()
            print "Settings loaded successful!"
        else:
            print "Error unable to load settings!!!"


    def get_hostkey(self, hostname):
        """
        Reads server hostkeys from ~/.ssh/known_hosts and sets self.hostkey
        """

        print "get_hostkeys()"

        hostkeytype = None
        hostkey = None

        try:
            host_keys = paramiko.util.load_host_keys(
                             os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            print '*** Unable to open host keys file'
            host_keys = {}

        if host_keys.has_key(hostname):
            hostkeytype = host_keys[hostname].keys()[0]
            self.hostkey = host_keys[hostname][hostkeytype]
            print 'Using host key of type %s' % hostkeytype

        print hostkeytype
        print self.hostkey


    def connect_sftp(self):
        """
        Connects to the FTP Server via sFTP from paramiko module
        """

        self.get_hostkey(self.server_adress)
        print "get_hostkey = OK"

        self.sftp_transport = paramiko.Transport((self.server_adress,
                                              int(self.server_port)))
        print "sftp_transport = OK"

        self.sftp_transport.connect(username=self.server_user,
                                    password=self.server_pass,
                                    hostkey=self.hostkey)
        print "sftp.connect = OK"

        self.sftp = paramiko.SFTPClient.from_transport(self.sftp_transport)
        print "sftp client = OK"

        self.sftp.chdir(self.server_folder)
        print "sftp chdir = OK"


    def upload(self, data):
        f = open(data, 'r')
        name = os.path.split(data)
        name = name[-1]

        print "File to upload: "+str(name)

        try:
            print "Start sFTP upload"
            self.connect_sftp()
            self.sftp.put(data, name)
            print "File uploaded"

            self.sftp_transport.close()

            print "sFTP upload finished."
            print "Success"
            return True

        except:
            print "Fail"
            return False


    def test_upload(self):
        """
        Method which could be called to test the upload function
        """

        test_file = "/opt/FotoShareN9/fotoshare_test_file"
        try:
            self.upload(test_file)
            print "sFTP upload works!"
            return True
        except:
            print "sFTP upload failed!"
            return False


if __name__ == "__main__":
    SftpUploadPlugin().test_upload()
