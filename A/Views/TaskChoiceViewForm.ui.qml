import QtQuick 2.4
import QtQuick.Controls 2.3

Item {
    id: element
    property alias logoutButton: logoutButton
    Button {
        id: logoutButton
        x: 256
        y: 261
        text: qsTr("Wyloguj")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}
