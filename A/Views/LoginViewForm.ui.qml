import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

Item {
    property alias loginButton: loginButton
    property alias busyIndicator: busyIndicator
    property alias loginNameInput: loginNameInput
    property alias loginPasswordInput: loginPasswordInput
    property alias loginErrorText: loginErrorText
    property alias registrationViewLink: registrationViewLink

    Column {
        id: column
        spacing: 10
        anchors.fill: parent

        Text {
            id: element
            text: qsTr("Logowanie")
            font.pointSize: 15
            anchors.horizontalCenter: parent.horizontalCenter
            horizontalAlignment: Text.AlignHCenter
        }

        Label {
            id: label
            text: qsTr("Login")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ComboBox {
            id: loginNameInput
            textRole: qsTr("")
            editable: true
            model: ListModel {
            }
            width: loginPasswordInput.width
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Label {
            id: label1
            text: qsTr("Hasło")
            anchors.horizontalCenter: parent.horizontalCenter
            horizontalAlignment: Text.AlignHCenter
        }

        TextField {
            id: loginPasswordInput
            text: qsTr("")
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: loginErrorText
            color: "#ff0000"
            text: qsTr(" ")
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        Button {
            id: loginButton
            text: qsTr("Zaloguj")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        BusyIndicator {
            id: busyIndicator
            spacing: 0
            visible: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: registrationViewLink
            text: qsTr("rejestracja urządzenia")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}




/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:1;anchors_height:400;anchors_width:200;anchors_x:72;anchors_y:41}
}
 ##^##*/
