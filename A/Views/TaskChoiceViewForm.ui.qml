import QtQuick 2.4
import QtQuick.Controls 2.3

Item {
    id: element
    property alias logoutButton: logoutButton
    property alias busyIndicator: busyIndicator
    property alias confirmButton: confirmButton
    property alias brigadeChoice: brigadeChoice
    property alias requestErrorText: requestErrorText
    property alias lineChoice: lineChoice

    Column {
        id: column
        spacing: 10
        anchors.fill: parent

        Text {
            id: element1
            text: qsTr("Zadanie")
            font.pointSize: 15
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: element2
            text: qsTr("Linia")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ComboBox {
            id: lineChoice
            editable: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: element3
            text: qsTr("Brygada")
            font.pointSize: 11
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ComboBox {
            id: brigadeChoice
            editable: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: requestErrorText
            color: "#fb0000"
            text: qsTr(" ")
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        Button {
            id: confirmButton
            text: qsTr("Ok")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        BusyIndicator {
            id: busyIndicator
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: logoutButton
            text: qsTr("Wyloguj")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}




/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:1;anchors_height:400;anchors_width:200;anchors_x:205;anchors_y:66}
}
 ##^##*/
