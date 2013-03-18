import QtQuick 1.1
import com.nokia.meego 1.0
import Qt 4.7

Page {
    id: settingsWindow
    tools: settingsTools
    orientationLock: PageOrientation.LockPortrait

    property alias servicesListModel: servicesListModel

    ToolBarLayout {
        id: settingsTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                pageStack.replace(Qt.resolvedUrl("MainPage.qml"))
            }
        }

        ToolButton {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Connection Test"
            onClicked: {
                plugin.test_connections()
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
        font.pixelSize: 48
        color: "#2489e0"
    }

    Text {
        id: connectionTypeSelectionText
        anchors.left: parent.left
        anchors.top: title.bottom
        anchors.leftMargin: 20

        color: "white"
        text: "Connection plugins"
        font.pixelSize: 40
        font.family: "Nokia Pure Text Light"
    }

    ListView {
        id: connectionTypsListView
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: connectionTypeSelectionText.bottom
        anchors.topMargin: 5

        width: 440
        height: 600
        clip: true

        model: ListModel {id: servicesListModel}
        delegate: ServiceDelegator{}
    }
}

