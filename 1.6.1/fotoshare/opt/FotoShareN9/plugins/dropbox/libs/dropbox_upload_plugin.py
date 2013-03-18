
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle

import dropbox
import oauth
import simplejson

class DropboxUploadPlugin:
    def __init__(self):

        print "Init DropboxUploadPlugin"

        # fill in YOUR application account secrets
        self.APP_KEY = ''
        self.APP_SECRET = ''
        self.ACCESS_TYPE = 'app_folder'

        self.config_path = '/home/user/.config/FotoShareN9/fotoshare_dropbox_plugin.cfg'

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            self.access_token = l['db_access_token']
            self.access_secret = l['db_access_secret']
        else:
            self.access_token = None
            self.access_secret = None


    def upload(self, data):
        """
        Uploads the file given with the path in 'data'
        """

        print "data am start"
        print data
        print type(data)

        with open(data) as f:
            name = os.path.split(data)
            name = name[-1]

            print "File to upload: "+str(name)

            try:
                print "Start Dropbox upload"
                session = dropbox.session.DropboxSession(self.APP_KEY,
                                                         self.APP_SECRET,
                                                         self.ACCESS_TYPE)

                print "session established"

                session.set_token(self.access_token, self.access_secret)

                print "token is set"

                client = dropbox.client.DropboxClient(session)

                print "client is online"

                #f = open(data)
                client.put_file(name, f)

                print "file was put to dropbox"

                print "Dropbox upload finished!"
                print "Success"
                return True

            except:
                print "Fail"
                return False


    def test_upload(self):
        """
        Method which could be called to test the upload function
        """

        #test_file = "/opt/FotoShareN9/fotoshare_testfile"
        test_file = "/opt/FotoShareN9/fotoshare_test_file"
        try:
            self.upload(test_file)
            print "Dropbox upload works!"
            return True
        except:
            print "Dropbox upload failed!"
            return False


if __name__ == "__main__":
    DropboxUploadPlugin().test_upload()
