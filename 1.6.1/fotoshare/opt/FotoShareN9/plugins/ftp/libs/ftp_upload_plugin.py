
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle
import ftplib


class FtpUploadPlugin:
    def __init__(self):

        self.config_path = '/home/user/.config/FotoShareN9/fotoshare_ftp_plugin.cfg'

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            # normal settings
            self.server_adress = l['server']
            self.server_port = l['port']
            self.server_folder = l['path'] 
            self.server_user = l['username']
            self.server_pass = l['pass']

            print "Settings aus FtpUploadPlugin:"
            print self.server_adress
            print self.server_port
            print self.server_folder
            print self.server_user
            print self.server_pass
            print type(self.server_adress)
            print type(self.server_port)
            print type(self.server_folder)
            print type(self.server_user)
            print type(self.server_pass)

            f.close()
            print "Settings loaded successful!"
        else:
            print "Error unable to load settings!!!"


    def connect_ftp(self):
        """
        Connects to the ftp server with known settings.
        """
        self.ftp = ftplib.FTP()
        print "FTP Instanz"

        self.ftp.connect(str(self.server_adress), str(self.server_port))
        print "FTP Verbindung"

        self.ftp.login(str(self.server_user), str(self.server_pass))
        print "FTP login"

        self.ftp.cwd(str(self.server_folder))
        print "FTP Verzeichnis wechsel!"


    def upload(self, data):
        f = open(data, 'r')
        name = os.path.split(data)
        name = name[-1]

        print "File to upload: "+str(name)

        print "Start FTP upload"
        self.connect_ftp()
        self.ftp.storbinary('STOR '+name, f)

        print "FTP upload finished!"
        print "Success"
        return True


    def test_upload(self):
        """
        Method which could be called to test the upload function
        """

        test_file = "/opt/FotoShareN9/fotoshare_test_file"
        try:
            self.upload(test_file)
            print "FTP upload works!"
            return True
        except:
            print "FTP upload failed!"
            return False


if __name__ == "__main__":
    FtpUploadPlugin().test_upload()
