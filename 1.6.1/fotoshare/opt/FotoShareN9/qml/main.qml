import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow

    initialPage: mainPage

    property string issue_connections: ""

    MainPage {
        id: mainPage
    }

    SettingsPage {
        id: settingsPage
    }

    function create_services_listview(list) {
        var i = 0
        settingsPage.servicesListModel.clear()
        for (i = 0; i<list.length; i++){
            //"qmlpath" is used in ServicesDelegator to create a dynamic QML page from the file the path tells
            settingsPage.servicesListModel.append({"name": list[i], "info": list[i+1], "qmlpath":list[i+2]})
            i = i+2
        }
    }

    function show_connection_test_result(str) {
        if (str == "") {conTestResult_good.open()}
        else if (str == "OFFLINE") {conTestResult_offline.open()}
        else {issue_connections = str;
              conTestResult_bad.open()}
    }

    function updateLogText(status) {
        if (status === "yes") { logMenuItem.text = "Disable logfile"}
        else { logMenuItem.text = "Enable logfile"}
    }

    QueryDialog {
        id: conTestResult_good
        titleText: "Result: Works"
        message: "All your activated connections were tested and seems to work as expected!"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: conTestResult_bad
        titleText: "Error: Problems"
        message: "The following connections are NOT working as expected, check your settings again:<br><br><font size='3'>"+issue_connections+"</font>"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: conTestResult_offline
        titleText: "Error: Offline"
        message: "Your Nokia N9 or N950 device is OFFLINE at the moment - activate any internet connection and try the connection test again please!"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: aboutDialog
        titleText: "About FotoShareN9"
        message: "FotoShareN9 shares your pictures to Dropbox, or a server of your choice.<br><br>
                  FotoShareN9 is open source software. The source code is/will be available at Github.com/AlphaX2/FotoshareN9<br><br>
                  <b>Author:</b> Gabriel Böhme<br>
                  <b>Licence:</b> GPL 3.0<br>
                  <b>Version:</b> 1.6.1<br><br>
                  <b>Thanks:</b><br> merlin1991, cermit3273, taviman, StefanX, opensmartpad.org for their help and ideas, also pexpect, Paramiko, Wazapp for sharing their code!"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: resetDialog
        titleText: "Warning!"
        message: "This will delete all your FotoShareN9 and Plugin settings. FotoShareN9 will close itself!"
        acceptButtonText: "Ok"
        rejectButtonText: "Cancel"

        onAccepted: {
            //reset settings in program logic
            main.reset_settings()
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
                // menu must be closed to prevent that the menu lay
                // above the settings page.
                if (myMenu.status == DialogStatus.Open) {myMenu.close()}

                // load listview with plugins and open settings page
                main.load_services()
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
                text: config.check_log_file_enabled() ? qsTr("Disable logfile") : qsTr("Enable logfile")
                onClicked: main.enable_log()
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
