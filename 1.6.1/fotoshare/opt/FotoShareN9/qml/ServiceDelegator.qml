import QtQuick 1.1
import com.nokia.meego 1.0

Component {
    Item {
        id: servicesDelegator

        width: 440
        height: 100

        property bool page_status: false

        Component.onCompleted: {
            page_status = true
        }

        function check_switch_status() {
            var model = settingsPage.servicesListModel
            var connection_name = model.get(index).name
            return plugin.check_connection_active(connection_name)
        }

        function enable_switch_status() {
            var model = settingsPage.servicesListModel
            var connection_name = model.get(index).name
            return plugin.check_connection_settings(connection_name)
        }

        Rectangle {
            id: background
            anchors.fill: servicesDelegator
            color: "grey"
            radius: 10
            opacity: mouseArea.pressed ? 0.5 : 0.0
        }

        MouseArea {
            id: mouseArea
            anchors.fill: servicesDelegator
            onClicked: {
                console.log(qmlpath)
                 pageStack.push(Qt.resolvedUrl(qmlpath))

            }
        }

        Row {
            anchors.verticalCenter: servicesDelegator.verticalCenter
            spacing: 30

            Switch {

                // did the user activate the plugin
                checked: check_switch_status()
                // are there saved settings = is it possible to activate it?
                enabled: enable_switch_status()

                onCheckedChanged: {
                    if (page_status === true) {
                    var model = settingsPage.servicesListModel
                    var connection_name = model.get(index).name
                    main.save_connections(connection_name)
                    }
                }
            }

            Column {
                Text {
                    text: name
                    color: "white"
                    font.family: "Nokia Pure Text"
                    font.bold: true
                    font.pixelSize: 24
                }

                Text {
                    text: info
                    color: "lightgrey"
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 16
                }
            }
        }

        Image {
            anchors.right: parent.right
            anchors.verticalCenter: servicesDelegator.verticalCenter
            source: "image://theme/icon-m-common-drilldown-arrow-inverse"
        }
    }
}
