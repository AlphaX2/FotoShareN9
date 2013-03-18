
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle

import pexpect
import paramiko

class ScpUploadPlugin:
    def __init__(self):

        self.config_path = '/home/user/.config/FotoShareN9/fotoshare_scp_plugin.cfg'


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


    def upload(self, data):
        """
        Managing all scp realted uploads
        """

        print "upload() method for upload via SCP starting"
        print data

        f = open(data, 'r')
        name = os.path.split(data)
        name = name[-1]

        print "File to upload: "+str(name)

        print "Start SCP upload"
        dest = self.server_user+'@'+self.server_adress+':/'+self.server_folder
        print "The destination is: "+dest

        self.get_hostkey(self.server_adress)

        # get files at .ssh - "id_rsa" would be the public key
        try:
            files_at_ssh = os.listdir('/home/user/.ssh')
        except:
            files_at_ssh = []

        print "files at ssh: "
        print files_at_ssh

        if not os.path.isdir('/home/user/.ssh'):
            print "scp: no ~/.shh found"
            try:
                print data
                print dest
                scp = pexpect.spawn('scp {0} {1}'.format(str(data), dest))
                scp.expect("Are you sure you want to continue connecting (yes/no)?")
                scp.sendline("yes")
                scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                scp.sendline(self.server_pass)
                scp.wait()

                print "SCP upload finished"
                print "Success"
                return True

            except:
                print "SCP upload failed"
                return False


        elif 'known_hosts' in files_at_ssh:
            print "scp: no publickey found"
            try:
                print data
                print dest

                scp = pexpect.spawn("scp {0} {1}".format(data, dest), timeout = 10000)
                print "spawn scp process - Ok"
                scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                print "expected password check - Ok"
                scp.sendline(self.server_pass)
                print "send password line - Ok"
                scp.wait()

                print "SCP upload finished"
                print "Success"
                return True

            except:
                print "SCP upload failed"
                return False


        elif self.hostkey and 'id_rsa' in files_at_ssh:
            print "scp: publickey found"
            try:
                print data
                print dest
                scp_string = 'scp {0} {1}'.format(str(data), dest)
                print scp_string

                scp = pexpect.spawn(scp_string)
                scp.expect("Enter passphrase for key '/home/user/.ssh/id_rsa: ")
                scp.sendline(self.server_pass)
                scp.wait()

                print "SCP upload finished"
                print "Success"
                return True

            except:
                print "SCP upload failed"
                return False


    def test_upload(self):
        """
        Method which could be called to test the upload function
        """

        test_file = "/opt/FotoShareN9/fotoshare_test_file"
        try:
            self.upload(test_file)
            print "SCP test upload works!"
            return True
        except:
            print "SCP test upload failed!"
            return False


if __name__ == "__main__":
    ScpUploadPlugin().test_upload()
