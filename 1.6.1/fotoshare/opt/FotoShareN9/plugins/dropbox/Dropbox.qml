import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    orientationLock: PageOrientation.LockPortrait
    tools: settingsTools

    /*Registering and loading your plugin is mandatory to use your
    functions from <plugin_name>_settings_handler! You can use your 
    functions in the following way:

    <plugin_name>_plugin.<function_name>()
    */

    Component.onCompleted: {
        plugin.register_plugin("dropbox")
        plugin.load_plugin()

        // JavaScript function to set the authentification buttons
        // text related to actual state (linked / not linked). Gets
        // data from Qt Property via Python
        set_auth_button_text()
    }

    function set_auth_button_text() {
        dropboxAuthButton.text = dropbox_plugin.button_text
}

    ToolBarLayout {
        id: settingsTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                main.load_services()
                pageStack.pop()
            }
        }
    }

        Text {
        id: title
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 20
        anchors.topMargin: 20

        text: "Settings"
        font.family: "Nokia Pure Text Light"
        font.pixelSize: 40
        color: "#2489e0"
    }

    Text {
        id: subtitle
        anchors.left: parent.left
        anchors.top: title.bottom
        anchors.leftMargin: 20

        color: "lightgrey"
        text: "Dropbox settings"
        font.pixelSize: 40
        font.family: "Nokia Pure Text Light"
    }

        Image {
        id: dropboxLogo

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 400
        source: "img/dropbox-logo.png"
        width: 330
        height: 112
    }

    Button {
        id: dropboxAuthButton

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 300
        text: "Link Dropbox"

        onClicked: {
            var state = dropboxAuthButton.text

            if (state === "Link Dropbox"){
                dropbox_plugin.get_dropbox_auth_weblink()
                dropboxAuthButton.text = "Ok"
                }

            if (state === "Ok"){
                dropbox_plugin.save_dropbox_auth_token()
                dropboxAuthButton.text = "Unlink Dropbox"
                }

            if (state === "Unlink Dropbox") {
                dropbox_plugin.unlink_dropbox_connection()
                dropboxAuthButton.text = "Link Dropbox"
                }
        }
    }

    Text {
        id: dropboxTermsLink

        anchors.top: dropboxAuthButton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 100
        text: "Dropbox terms and privacy"
        color: openTermsLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        font.bold: true
        visible: true

        MouseArea {
            id: openTermsLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally("https://www.dropbox.com/terms/")}
        }
    }
}
