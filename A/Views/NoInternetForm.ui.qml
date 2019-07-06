import QtQuick 2.4
import QtQuick.Controls 2.3

Item {
    id: element1
    property alias retryButton: retryButton

    Column {
        id: column
        spacing: 2
        anchors.fill: parent

        Text {
            id: element
            width: 158
            height: 60
            color: "#ff0404"
            text: qsTr("Brak połączenia z internetem")
            font.family: "Verdana"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
        }

        Button {
            id: retryButton
            text: qsTr("Spróbuj ponownie")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}




/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:1;anchors_height:400;anchors_width:200;anchors_x:94;anchors_y:31}
}
 ##^##*/
