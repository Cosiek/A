import QtQuick 2.4
import QtQuick.Controls 2.3

Item {
    property alias saveButton: saveButton
    property alias keyInput: keyInput
    property alias idInput: idInput
    property alias busyIndicator: busyIndicator
    property alias backButton: backButton
    property alias errorText: errorText

    Column {
        id: column
        spacing: 3
        anchors.rightMargin: 3
        anchors.leftMargin: 3
        anchors.bottomMargin: 3
        anchors.topMargin: 3
        anchors.fill: parent

        Button {
            id: backButton
            width: 25
            height: 25
            text: qsTr("←")
        }

        Text {
            id: element
            text: qsTr("Identyfikator")
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        TextField {
            id: idInput
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 15
        }

        Text {
            id: element1
            text: qsTr("Klucz")
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        TextField {
            id: keyInput
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 15
        }

        Text {
            id: errorText
            color: "#ff0000"
            text: qsTr(" ")
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        BusyIndicator {
            id: busyIndicator
            running: false
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: saveButton
            text: qsTr("Zapisz")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}




/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
