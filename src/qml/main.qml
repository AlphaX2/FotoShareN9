import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow

    initialPage: mainPage

    function updateSettingsText(server, path, user, pass, connect, port) {
        console.log("Settings werden aktualisiert!")
        settingsPage.serverField = server
        settingsPage.pathField = path
        settingsPage.userField = user
        settingsPage.passField = pass
        settingsPage.portField = port

        if (connect === "ftp"){settingsPage.ftpChecked = true}
        if (connect === "sftp"){settingsPage.sftpChecked = true; settingsPage.selectedConnectionType = "sftp"}
        if (connect === "scp"){settingsPage.scpChecked = true; settingsPage.selectedConnectionType = "scp"}
    }

    function update_dropbox_auth_button(status, url) {
        if (status === "Ok") {settingsPage.dropboxURL = url; settingsPage.authButton = status}
        else {settingsPage.authButton = status}
    }

    //if activate switch is checked, also daemon startup switch will be enabled
    function switchCHECKED(checked) {
        if (checked === "true") {mainPage.switcherCHECK = true}
        else {mainPage.switcherCHECK = false}
    }

    function switchON(firstStart) {
        if (firstStart === "true"){mainPage.switcherENABLE = true; settingsPage.conButton = 1.0}
        else {mainPage.switcherENABLE = false; settingsPage.conButton = 0.0}
    }

    function switchDaemonONOFF() {
        mainPage.switcherStartupENABLE = true
    }

    function switchDaemonCHECK() {
        mainPage.switcherStartupCHECK = true
    }

    function switchResizeONOFF() {
        console.log("QML: switchResize will be enabled")
        mainPage.switcherResizeENABLE = true
    }

    function switchResizeCHECK(size) {
        console.log("QML: Resize Slider is set to: "+size)
        mainPage.switcherResizeCHECK = true;
        mainPage.resizeSliderValue = size
    }

    function uploadTypeButtonENABLED() {
        console.log("QML: uploadTypeButton will be enabled")
        mainPage.uploadTypeButtonENABLE = true
    }

    function intervalUploadCHECKED(time) {
        mainPage.intervalButtonCHECK = true
        console.log("QML: Interval is set to: "+time)
        if (time === "5"){mainPage.interval5 = true}
        if (time === "10"){mainPage.interval10 = true}
        if (time === "15"){mainPage.interval15 = true}
        if (time === "30"){mainPage.interval30 = true}
        if (time === "45"){mainPage.interval45 = true}
        if (time === "60"){mainPage.interval60 = true}
    }

    function notificationTypeButtonENABLED() {
        console.log("QML: notificationButton will be enabled")
        mainPage.notifyButtonENABLE = true
    }

    function notificationTypeButtonCHECKED(typus) {
        console.log("QML: NotificationButton will be checked with: "+typus)
        if (typus === "banner"){mainPage.notifyButtonBannerCHECK = true}
        if (typus === "EventFeed"){mainPage.notifyButtonEventCHECK = true}
    }

    function videoUploadButtonENABLED() {
        console.log("QML: videoUploadButton will be enabled")
        mainPage.videoUploadENABLE = true
    }

    function videoUploadButtonCHECKED() {
        mainPage.videoUploadCHECK = true
    }

    function wifi3GButtonENABLED() {
        console.log("QML: wifi/3G Button will be enabled")
        mainPage.wifi3GENABLE = true
    }

    function wifiButtonCHECKED() {
        mainPage.wifiCHECK = true
    }

    function callConnectionDialog(str) {
        if (str === "ok") {connectionDialogOK.open()}
        else {connectionDialogFail.open()}
    }

    function updateLogText(status) {
        if (status === "yes") { logMenuItem.text = "Disable logfile"}
        else { logMenuItem.text = "Enable logfile"}
    }

    MainPage {
        id: mainPage
    }

    SettingsPage {
        id: settingsPage
    }

    QueryDialog {
        id: connectionDialogOK
        titleText: "Result: Works"
        message: "Your server settings seems to be right!"
    }

    QueryDialog {
        id: connectionDialogFail
        titleText: "Result: Fails"
        message: "Your server settings seems NOT to be right! Please check your internet connection and your server settings and try it again!"
    }

    QueryDialog {
        id: aboutDialog
        titleText: "About FotoShareN9"
        message: "FotoShareN9 shares your pictures to Dropbox, or a server of your choice.<br><br>
                  FotoShareN9 is open source software. The source code is/will be available at Github.com/AlphaX2/FotoshareN9<br><br>
                  <b>Author:</b> Gabriel Böhme<br>
                  <b>Licence:</b> GPL 3.0<br>
                  <b>Version:</b> 0.9.7<br><br>
                  <b>Thanks:</b><br> merlin1991, cermit3273, opensmartpad.org for their help and ideas, also pexpect, Paramiko, Wazapp for sharing their code!"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: resetDialog
        titleText: "Warning!"
        message: "This will delete all your FotoShareN9 settings."
        acceptButtonText: "Ok"
        rejectButtonText: "Cancel"

        onAccepted: {
            //disable all buttons on UI

            // Main activation switcher
            mainPage.switcherENABLE = false
            mainPage.switcherCHECK = false      //will also disable daemon if running

            // Daemon on startup switch
            mainPage.switcherStartupENABLE = false
            mainPage.switcherStartupCHECK = false

            // Resize switch
            mainPage.switcherResizeENABLE = false
            mainPage.switcherResizeCHECK = false
            mainPage.resizeSliderValue = 50

            // notifications ButtonRow
            mainPage.notifyButtonENABLE = false
            mainPage.notifyButtonOffCHECK = true

            // video upload ButtonRow
            mainPage.videoUploadENABLE = false
            mainPage.videoUploadCHECK = false

            // interval upload ButtonRow
            mainPage.uploadTypeButtonENABLE = false
            mainPage.intervalButtonCHECK = false

            // Wifi&3G or Wifi only upload ButtonRow
            mainPage.wifiCHECK = false
            mainPage.wifi3GENABLE = false

            //reset settings in program logic
            controller.settings_reset_signal()
        }
    }

    QueryDialog {
        id: privacyDialog
        titleText: "Privacy policy"

        message: "FotoShareN9 will collect the login information you give in the settings and nothing more. Your login data is stored in a configuration file on your device and nowhere else. FotoShareN9 will only use it to establish connections to the available services and/or servers. The login data is not given to any third party and is not used for any other purpose than the functions of FotoShareN9.<br><br> If you have any questions, concerns, or comments about our privacy policy you may contact us via:<br>m.gabrielboehme@googlemail.com"

        acceptButtonText: "Ok"
    }

    ToolBarLayout {
        id: commonTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (myMenu.status === DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }

        ToolButton {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Server settings"
            onClicked: {
                controller.load_settings_signal()
                pageStack.push(settingsPage)
            }
        }
    }

    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem {
                text: qsTr("Reset settings")
                onClicked: {
                    resetDialog.open()
                }
            }

            MenuItem {
                id: logMenuItem
                text: qsTr("Enable logfile")
                onClicked: controller.enable_log_file_signal()
            }

            MenuItem {
                text: qsTr("Privacy policy")
                onClicked: privacyDialog.open()
            }

            MenuItem {
                text: qsTr("About")
                onClicked: aboutDialog.open()
            }

        }
    }
}
