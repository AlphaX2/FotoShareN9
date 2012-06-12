#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import ftplib
import pickle
import subprocess

import paramiko
import pexpect
import oauth
import dropbox

from PySide import QtCore
from PySide.QtCore import Qt
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL

class FotoShareN9(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.FOTOSHARE_VERSION = "0.9.7"

        #Oberfläche und Instanzierungen für QML2Py Funktionen
        self.view = QtDeclarative.QDeclarativeView()

        #OpenGL Rendering
        self.glw = QtOpenGL.QGLWidget()
        self.view.setViewport(self.glw)

        self.view.setSource(QtCore.QUrl('/opt/FotoShareN9/qml/main.qml'))
        self.root = self.view.rootObject()

        #instantiate the Python object
        self.controller = Controller()

        #expose the object to QML
        self.context = self.view.rootContext()
        self.context.setContextProperty('controller', self.controller)

        self.config_path = '/home/user/.config/fotoshare.cfg'

        #loads all important data and settings
        self.preload_settings()

        #Holds pid of daemon, if running, else it's empty.
        self.pid = ''

        #returns the pid of a running daemon to self.pid
        self.getPID()
        print "The daemons PID is: "+str(self.pid)

        #set GUI Buttons etc. depending from settings ----------------
        #check for first start
        self.is_first_start()

        #create new settings cfg if version needs new one
        self.check_version()

        #check if daemon boots on startup and set slider on GUI
        self.check_daemon_startup()

        #check resize switch and slider
        self.check_resize_options()

        #check other options from GUI ButtonRows
        self.check_button_options()

        #check that dropbox is linked or not and show on UI
        self.check_dropbox_link()

        #Change menu text in dependency to log status in cfg
        self.check_log_file()

        #holds ssh hostkey
        self.hostkey = None

        #Holds dropbox appkey and app secret for authentification
        self.APP_KEY = 'uvxyouqhkdljbdn'
        self.APP_SECRET = '09sd2chtvifn5aj'
        self.ACCESS_TYPE = 'app_folder'

    #Connections from Controller() class for QML/Py communication
        self.controller.signal_settings_saver.connect(self.save_settings)
        self.controller.signal_settings_loader.connect(self.load_settings)

        #Connection for daemon start
        self.controller.signal_daemon_on_off.connect(self.start_stop_daemon)

        #Connection for daemon on boot option
        self.controller.signal_startupDaemon.connect(
                                        self.activate_startup_daemon)

        #Connection for resize switch/slider
        self.controller.signal_resize_photos.connect(self.save_resize_option)

        #Connections for option ButtonRow elements
        self.controller.signal_notification_select.connect(self.save_notification_type)
        self.controller.signal_video_select.connect(self.save_video_upload_option)
        self.controller.signal_wifi3g_select.connect(self.save_wifi3g_option)
        self.controller.signal_upload_type_select.connect(self.save_upload_type)
        self.controller.signal_save_interval_time.connect(self.save_interval_times) #TIMES not TIME! ;)

        #Test connections and settings set in GUI
        self.controller.signal_contest.connect(self.test_connection)

        #Reset all settings
        self.controller.signal_settings_reset.connect(self.reset_settings)

        #Activate LOG File
        self.controller.signal_activate_log.connect(self.enable_log)

        #Dropbox authentification process stuff
        self.controller.signal_dropbox_authweb.connect(
                                       self.get_dropbox_auth_weblink)

        self.controller.signal_dropbox_authsave.connect(
                                       self.save_dropbox_auth_token)

        self.controller.signal_dropbox_unlink.connect(
                                       self.unlink_dropbox_connection)

# Preload all relevant information -----------------------------------

    def preload_settings(self):
        """
        Loading settings from cfg if possible, or load default settings.

        If it was not able to load settings something went wrong, or 
        there is just no file: load default settings. Also version
        of last FotoShareN9 version is loaded and will later be checked
        that there is no newer one - if so create new cfg.
        """

        # Preload all relevant data from settings:
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            print "--------------------------------------------------"
            print
            print "These are the settings:"
            print
            print l
            print

            try:
                self.server_adress = l['server']
                self.server_folder = l['path'] 
                self.server_user = l['username']
                self.server_pass = l['pass']
                self.server_port = l['port']
                self.connection_type = l['connection']
                self.connection_radio = l['data_connection']
                self.upload_type = l['upload_type']
                self.daemon_startup = l['daemon_startup']
                self.db_sync_status = l['db_sync']
                self.access_token = l['db_access_token']
                self.access_secret = l['db_access_secret']
                self.video_upload = l['video_upload']
                self.interval_time = l['interval_time']
                self.version = l['version']
                self.log = l['log']
                self.resize = l['resize']
                self.notification_type = l['notification_type']
            except:
                self.version = None

            print "Version is:"+str(self.version)

        else:
            self.server_adress = ''
            self.server_folder = ''
            self.server_user = ''
            self.server_pass = ''
            self.server_port = ''
            self.connection_type = ''
            self.connection_radio = '3G'
            self.upload_type = 'instant'
            self.daemon_startup = ''
            self.db_sync_status = 'False'
            self.access_token = ''
            self.access_secret = ''
            self.video_upload = 'forbidden'
            self.interval_time = 5
            self.version = self.FOTOSHARE_VERSION
            self.log = 'no'
            self.notification_type = 'off'
            self.resize = 0


    def getPID(self):
        """
        Parses the pid of the fotoshare_service daemon and set the
        number to self.pid. Also updates switch in the GUI if it is
        running on app start.
        """

        cmd = 'ps aux|grep python'
        pid = os.popen(cmd)
        data = pid.readlines()

        for i in data:
            if 'fotoshare_service' in i:
                daemon_pid = re.findall(r'\b\d+\b', str(i))
                self.pid = daemon_pid[0]
                self.root.switchCHECKED('true')
                print 'Daemons pid is: '+daemon_pid[0]

# pre GUI startup checks like options/switches -----------------------

    def is_first_start(self):
        """
        check for first start - set switch in QML UI
        """

        # if os.path.isfile(self.config_path):
        if self.server_adress == '' and self.db_sync_status == 'False':
            print "This is first start/no server settings."
            self.root.switchON('false')
        else:
            print "This is not first start: found server settings"
            self.root.switchON('true')


    def check_version(self):
        """
        Check the version of cfg and creates a new one if no version
        key can be found, or a new FotoShareN9 version is detected.
        If there is a newer version detected, it will reset all data
        to be sure that a new and working config is generated!
        """

        if self.version == None:
            print "No version controll found: create new cfg"
            self.reset_settings()
            self.root.switchON('false')
            self.start_stop_daemon() # stop daemon if running
        else:
            if not self.version == self.FOTOSHARE_VERSION:
                print "New FotoShareN9 version: reset and create new cfg."
                self.reset_settings()
                self.root.switchON('false')
                self.start_stop_daemon() # stop daemon if running


    def check_daemon_startup(self):
        """
        If daemon is allowed to start on boot set slider on UI to show it.
        """

        print "daemon_startup: "+str(self.daemon_startup)

        if self.daemon_startup == 'yes':
            print "Check startup slider: true"
            self.root.switchDaemonCHECK()


    def check_resize_options(self):
        """
        Check if resize is active and set slider on GUI to show it.
        """

        if self.resize > 0:
            print "Check resize slider: true"
            self.root.switchResizeCHECK(self.resize)


    def check_button_options(self):
        """
        Checks selected options from ButtonRows on MainPage and set GUI.
        """

        if self.notification_type != 'off':
            print "Notify type is: "+str(self.notification_type)
            self.root.notificationTypeButtonCHECKED(self.notification_type)

        # check for instant/interval upload
        if self.upload_type == 'interval':
            self.root.intervalUploadCHECKED(str(self.interval_time))

        # check if videoupload is allowed
        if self.video_upload == 'allowed':
            self.root.videoUploadButtonCHECKED()

        # check wifi only upload and set button
        if self.connection_radio == u'Wlan':
            self.root.wifiButtonCHECKED()

        # check for server settings if there are no details filled in
        # the buttons will stay disabled until the user fills in 
        # something.
        if not self.server_adress == '' or not self.db_sync_status == 'False':

            self.root.switchDaemonONOFF()
            self.root.switchResizeONOFF()

            self.root.wifi3GButtonENABLED()
            self.root.uploadTypeButtonENABLED()
            self.root.videoUploadButtonENABLED()
            self.root.notificationTypeButtonENABLED()


    def check_dropbox_link(self):
        """
        Check if Dropbox is linked or not and show it on UI button.
        """

        if self.access_token == '' and self.access_secret == '':
            print "Dropbox: not linked"
            print
            self.root.update_dropbox_auth_button('Link Dropbox', '')
        else:
            print "Dropbox: linked"
            print
            self.root.update_dropbox_auth_button('Unlink Dropbox', '')


    def check_log_file(self):
        """
        Set log file text in menu depending on the fact it is on/off
        """

        if self.log == 'yes':
            self.root.updateLogText('yes')
        else:
            self.root.updateLogText('no')

# all kinds off save and load functions ------------------------------

    def load_settings(self):
        """
        Load saved settings on GUI when "Server Settings" button is 
        clicked and the SettingsPage loading.
        """

        print "Load settings"
        self.root.updateSettingsText(self.server_adress,
                                     self.server_folder,
                                     self.server_user,
                                     self.server_pass,
                                     self.connection_type,
                                     self.server_port
                                     )
        print "Load ended."


    def save_settings(self, server, path, user, passw, connect, port):
        """
        Saves settings, which are set in the GUI SettingsPage.
        """

        # path should be without root "/" so terminate it here
        if path.startswith('/'):
            path = path[1:]

        # If not a server is selected changes connection type to "" for
        # preventing errors like senseless upload tries.
        if not server:
            connect = ''

        # update arguments for running app/window class
        self.server_adress = str(server)
        self.server_folder = str(path)
        self.server_user = str(user)
        self.server_pass = str(passw)
        self.connection_type = str(connect)
        self.server_port = str(port)

        # load config file or create a new one
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)
        else:
            f = open(self.config_path, 'w')
            pickle.dump(
                        {
                         'server':'',
                         'port':'',
                         'path':'',
                         'username':'',
                         'pass':'',
                         'connection':'',
                         'data_connection': '3G',
                         'daemon_startup': '',
                         'video_upload': 'forbidden',
                         'interval_time': 5,
                         'upload_type': 'instant',
                         'db_sync': 'False',
                         'db_access_token': '',
                         'db_access_secret': '',
                         'version': self.FOTOSHARE_VERSION,
                         'log': 'no',
                         'resize': 0,
                         'notification_type':'off'
                         }, f)

            f = open(self.config_path)
            l = pickle.load(f)

        l['server'] = str(server)
        l['port'] = str(port)
        l['path'] = str(path)
        l['username'] = str(user)
        l['pass'] = str(passw)
        l['connection'] = str(connect)

        # save config
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()


    def save_resize_option(self, percent):
        """
        Saves the selected resize option
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['resize'] = percent
            self.resize = percent

            print "Resize is now: "+str(self.resize)+" %"

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_notification_type(self, typus):
        """
        Saves the selected notification type
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['notification_type'] = str(typus)
            print "Notification type is now: "+str(typus)

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_video_upload_option(self, typus):
        """
        Saves setting from GUI: 'No video upload' vs. 'Video upload'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['video_upload'] = typus
            print "Video upload is now: "+str(typus)

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_wifi3g_option(self, radio):
        """
        Saves setting from GUI: 'Wifi only' vs. 'Wifi and 3G'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['data_connection'] = radio
            print "Upload is now: "+str(radio)

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_upload_type(self, typus):
        """
        Saves setting from GUI: 'Instant sync' vs. 'Inverval sync'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['upload_type'] = typus
            print "Upload type is now: "+str(typus)

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_interval_times(self, time):
        """
        Saves the selected interval time
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['interval_time'] = int(time)
            print "Interval upload time is now: "+str(time)+" Minutes."

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def enable_log(self):
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            if l['log'] == 'yes':
                l['log'] = 'no'
            else:
                l['log'] = 'yes'

            self.log = l['log']
            self.root.updateLogText(str(self.log))

            print "Is log active? "+str(self.log)

            # save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def reset_settings(self):
        """
        Deletes all configuration data and loads default.

        It will be called if user selected reset on the GUI and if a 
        new version of FotoShareN9 is started, which has more or less 
        options than the older version. So the user have to set 
        everything again, but don't have to delete it's cfg and sav 
        file by hand.

        After reset, preload_settings function create a new cfg and
        loads default settings.
        """

        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
            self.preload_settings()
        else:
            print "No reset is done, because no cfg file was found."

        if os.path.isfile("/home/user/.config/fotoshare_offline.sav"):
            os.remove("/home/user/.config/fotoshare_offline.sav")
        else:
            print "No _offline.sav found - do nothing."


# main functions -----------------------------------------------------


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


    def start_stop_daemon(self):
        """
        Starts and stops daemon from QML UI
        """

        if self.pid == '':
            print 'Daemon is not running and will start now!'
            subprocess.Popen(['/opt/FotoShareN9/fotoshare_service','&'])
            self.getPID()
        else:
            print 'Daemon was running and its PID was: '+str(self.pid)
            subprocess.Popen(['kill', '%d' %(int(self.pid))])
            self.pid = ''
            self.root.switchCHECKED('false')


    def activate_startup_daemon(self):
        """
        Python logic of QML Switch for starting daemon on boot or not.

        Sets an entry in fotoshare.cfg (yes/no) which holds the info
        about the daemon is allowed to run from boot or not. It will
        also be read by the daemon on startup, if set to "no" the daemon
        stops, otherwise stays on.
        """

        print "activate_startup_daemon"

        if os.path.isfile(self.config_path):
            # Laden der gespeicherten Werte
            f = open(self.config_path)
            l = pickle.load(f)

            daemon = l['daemon_startup']
            print daemon

            # 'yes' and 'no' is used, because True/False didn't work.
            if daemon == 'yes':
                status = ''
            if daemon == '':
                status = 'yes'

            print "Daemon startup is set to: "+status

            l['daemon_startup'] = status

        # Save data
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()

# Dropbox Handling----------------------------------------------------

#    Here you find three different functions:
#    1. generate a Dropbox authentication link
#    2. save tokens you got from Dropbox
#    3. Unlink Dropbox => delete tokens and clear Dropbox settings

#    It's handled by the Dropbox authentication button in QML so have
#    also a look there!


    def get_dropbox_auth_weblink(self):
        """
        Generates an authentication weblink for Dropbox and shows a
        link on the GUI.
        """

        print "Dropbox auth"
        self.drop_session = dropbox.session.DropboxSession(
                                                     self.APP_KEY,
                                                     self.APP_SECRET,
                                                     self.ACCESS_TYPE)

        self.request_token = self.drop_session.obtain_request_token()
        url = self.drop_session.build_authorize_url(self.request_token)

        # URL is only passed to GUI here
        self.root.update_dropbox_auth_button("Ok", url)


    def save_dropbox_auth_token(self):
        """
        Generates an access token from request token and saves them.
        """

        print "Dropbox save"
        # This will fail if the user didn't visit the Auth-URL and hit 'Allow'
        self.access_token = self.drop_session.obtain_access_token(
                                                   self.request_token)

        self.save_dropbox_settings(
                                    self.access_token.key,
                                    self.access_token.secret)

        # second argument is "" to have no link text anymore on GUI
        self.root.update_dropbox_auth_button('Unlink Dropbox', "")


    def unlink_dropbox_connection(self):
        """
        Destroys the link to Dropbox and reset settings.
        """

        print "Dropbox unlink"
        # If user want to destroy the connection from app to dropbox
        self.drop_session = None
        self.save_dropbox_settings('', '')
        self.root.update_dropbox_auth_button('Link Dropbox', '')


    def save_dropbox_settings(self, access_token, access_secret):
        """
        Saves Dropbox access token informations from authentification.

        If there is no settings file a new one will be created and
        filled up with default settings.
        """

        # load config file or create a new one
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)
        else:
            f = open(self.config_path, 'w')
            pickle.dump(
                        {
                         'server':'',
                         'port':'',
                         'path':'',
                         'username':'',
                         'pass':'',
                         'data_connection': '3G',
                         'connection':'',
                         'daemon_startup': '',
                         'upload_type': 'instant',
                         'video_upload': 'forbidden',
                         'interval_time': 5,
                         'db_sync': 'False',
                         'db_access_token': '',
                         'db_access_secret': '',
                         'version': self.FOTOSHARE_VERSION,
                         'log': 'no',
                         'notification_type':'off',
                         'resize': 0,
                         }, f)

            f = open(self.config_path)
            l = pickle.load(f)

        l['db_access_token'] = str(access_token)
        l['db_access_secret'] = str(access_secret)

        # Update them to be sure the open app has the newest informations.
        self.access_token = str(access_token)
        self.access_secret = str(access_secret)

        # Dropbox is not saved as connection type to allow the user
        # to sync both - Dropbox and a server as well.

        if self.access_token == '' and self.access_secret == '':
            l['db_sync'] = 'False'
            self.db_sync_status = 'False'
            print "Will Dropbox sync? "+str(self.db_sync_status)
        else:
            l['db_sync'] = 'True'
            self.db_sync_status = 'True'
            print "Will Dropbox sync? "+str(self.db_sync_status)

        # save config
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()

# Connection testing -------------------------------------------------

    def test_connection(self, con_type):
        """
        Function tests the settings and connection type set on the UI
        """

        # Try to connect via ftp
        if con_type == 'ftp':
            print 'Testing ftp connection...'
            try: 
                self.ftp = ftplib.FTP()
                self.ftp.connect(self.server_adress, self.server_port)
                self.ftp.getwelcome()
                self.root.callConnectionDialog('ok')
            except:
                self.root.callConnectionDialog('fail')

        # Try to connect via sftp
        if con_type == 'sftp':
            'Testing sftp connection...'
            self.get_hostkey(self.server_adress)
            try:
                t = paramiko.Transport((self.server_adress, 
                                        int(self.server_port)))

                t.connect(username=self.server_user,
                          password=self.server_pass,
                          hostkey=self.hostkey)

                sftp = paramiko.SFTPClient.from_transport(t)
                sftp.chdir(self.server_folder)
                t.close()
                self.root.callConnectionDialog('ok')
            except:
                self.root.callConnectionDialog('fail')

        # Try to connect via scp
        if con_type == 'scp':
            print 'Testing scp connection...'

            test = '/opt/FotoShareN9/scp_test_file'
            dest = self.server_user+'@'+self.server_adress+':/'+self.server_folder

            self.get_hostkey(self.server_adress)

            # Get files at .ssh for checking "fotoshare" named
            # publickey is in it.
            files_at_ssh = os.listdir('/home/user/.ssh')

            # check if there is .ssh - if not create known_hosts and
            # login via normal password.
            if not os.path.isdir('/home/user/.ssh'):
                print "scp: no ~/.shh found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    scp.expect("Are you sure you want to continue connecting (yes/no)?")
                    scp.sendline("yes")
                    scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')

                except:
                    print "SCP: except @ no .ssh dir"
                    self.root.callConnectionDialog('fail')

            # Without "fotoshare" publickey use normal password login.
            if self.hostkey and not 'fotoshare' in files_at_ssh:
                print "scp: no publickey found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')
                except:
                    print "SCP: except @ known_hosts only"
                    self.root.callConnectionDialog('fail')

            # Use publickey for upload (password means passphrase)
            if self.hostkey and 'fotoshare' in files_at_ssh:
                print "scp: publickey found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    # FotoShareN9 accept only a public key with the name "fotoshare"
                    scp.expect("Enter passphrase for key '/home/user/.ssh/fotoshare: ")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')
                except:
                    print "SCP: except @ public key auth"
                    self.root.callConnectionDialog('fail')


        # Try to connect via Dropbox
        if self.db_sync_status == 'True':
            print 'Testing Dropbox connection...'

            try:
                session = dropbox.session.DropboxSession(
                                                    self.APP_KEY,
                                                    self.APP_SECRET,
                                                    self.ACCESS_TYPE)

                session.set_token(self.access_token,
                                    self.access_secret)

                client = dropbox.client.DropboxClient(session)
                #print is used as a real part of the test!
                print client.account_info()
                self.root.callConnectionDialog('ok')

            except:
                self.root.callConnectionDialog('fail')


# Controller Class for QML to Python communication--------------------
class Controller(QtCore.QObject):
    """
    Controller class is connected to QML and receives signals, which
    are send from QML and connects them to Python functions.
    """

    # Dropbox related signals
    signal_dropbox_authweb = QtCore.Signal()
    signal_dropbox_authsave = QtCore.Signal()
    signal_dropbox_unlink = QtCore.Signal()

    # Save/load putted in settings from GUI
    signal_settings_saver = QtCore.Signal(str, str, str, str, str, str)
    signal_settings_loader = QtCore.Signal()

    # MainPage switches and buttons
    signal_daemon_on_off = QtCore.Signal()
    signal_startupDaemon = QtCore.Signal()
    signal_resize_photos = QtCore.Signal(int)

    signal_notification_select = QtCore.Signal(str)
    signal_video_select = QtCore.Signal(str)
    signal_wifi3g_select = QtCore.Signal(str)
    signal_upload_type_select = QtCore.Signal(str)
    signal_save_interval_time = QtCore.Signal(str)

    # Connection test from SettingsPage
    signal_contest = QtCore.Signal(str)

    # Menu Options
    signal_activate_log = QtCore.Signal()
    signal_settings_reset = QtCore.Signal()


    def __init__(self):
        QtCore.QObject.__init__(self)


    # Dropbox related signals
    @QtCore.Slot(str)
    def auth_dropbox_signal(self, status):
        if status == "web":
            self.signal_dropbox_authweb.emit()
        if status == "save":
            self.signal_dropbox_authsave.emit()
        if status == "unlink":
            self.signal_dropbox_unlink.emit()


    # Save and load settings from SettingsPage GUI
    @QtCore.Slot(str, str, str, str, str, str)
    def save_settings_signal(self, server, path, user, passw, connect, port):
        self.signal_settings_saver.emit(server, path, user, passw, connect, port)

    @QtCore.Slot()
    def load_settings_signal(self):
        self.signal_settings_loader.emit()


    # MainPage switches
    @QtCore.Slot()
    def start_daemon_signal(self):
        self.signal_daemon_on_off.emit()

    @QtCore.Slot()
    def activate_startup_daemon_signal(self):
        self.signal_startupDaemon.emit()

    @QtCore.Slot(int)
    def resize_photos_signal(self, percent):
        self.signal_resize_photos.emit(percent)


    # MainPage buttons
    @QtCore.Slot(str)
    def notification_select_signal(self, typus):
        self.signal_notification_select.emit(typus)

    @QtCore.Slot(str)
    def video_select_signal(self, typus):
        self.signal_video_select.emit(typus)

    @QtCore.Slot(str)
    def wifi3g_select_signal(self, radio):
        self.signal_wifi3g_select.emit(radio)

    @QtCore.Slot(str)
    def upload_type_select_signal(self, typus):
        self.signal_upload_type_select.emit(typus)

    @QtCore.Slot(str)
    def save_interval_time_signal(self, time):
        self.signal_save_interval_time.emit(time)


    # Connection Test from SettingsPage
    @QtCore.Slot(str)
    def test_connection_signal(self, con_type):
        self.signal_contest.emit(con_type)


    # Menu options
    @QtCore.Slot()
    def settings_reset_signal(self):
        self.signal_settings_reset.emit()

    @QtCore.Slot()
    def enable_log_file_signal(self):
        self.signal_activate_log.emit()



# Starting the app ---------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    start = FotoShareN9()
    start.view.showFullScreen()
    sys.exit(app.exec_())
