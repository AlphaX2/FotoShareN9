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
        plugin.register_plugin("googledrive")
        plugin.load_plugin()

        // JavaScript function to set the authentification buttons
        // text related to actual state (linked / not linked). Gets
        // data from Python
        set_auth_button_text()
    }

    function set_auth_button_text() {
            var button_text = googledrive_plugin.get_button_text()
            googledriveAuthButton.text = button_text
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
        text: "GoogleDrive settings"
        font.pixelSize: 40
        font.family: "Nokia Pure Text Light"
    }

        Image {
        id: flickrLogo

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 350
        source: "img/drive-logo.png"
        width: 200
        height: 200
    }

    Button {
        id: googledriveAuthButton

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 280
        text: "Link GoogleDrive"

        onClicked: {
            var status = googledriveAuthButton.text

            // opens auth web page
            if (status === "Link GoogleDrive") {
                googledrive_plugin.auth_googledrive()
                googledriveAuthButton.text = "Ok"
                }
            // just click ok to have same logic as in Dropbox, Flickr...
            if (status === "Ok") {
                googledriveAuthButton.text = "Unlink GoogleDrive"
                }
            // unlink will delete token file
            if (status === "Unlink GoogleDrive") {
                googledrive_plugin.unlink_googledrive()
                googledriveAuthButton.text = "Link GoogleDrive"
                }
        }
    }

    Text {
        id: googledriveTermsOfServiceLink

        anchors.top: googledriveAuthButton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 100
        text: "GoogleDrive Terms of Service"
        color: openTermsLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        font.bold: true
        visible: true

        MouseArea {
            id: openTermsLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally("http://www.google.com/apps/intl/en/terms/standard_terms.html")}
        }
    }

    Text {
        id: googledrivePrivacyPolicy

        anchors.top: googledriveAuthButton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 150
        text: "GoogleDrive privacy policy"
        color: openPrivacyLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        font.bold: true
        visible: true

        MouseArea {
            id: openPrivacyLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally("http://www.google.com/policies/privacy/")}
        }
    }
}
