import QtQuick 2.10
import QtQuick.Controls 2.1
import QtQuick.Window 2.10
import QtPositioning 5.10


Window {
    id: appWindow
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    StackView {
        id: stackView
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent
        initialItem: menuComponent
    }

    Component {
        id: menuComponent

        Column {
            id: menuComponentColumn
            spacing: 10

            Text {
                id: menuComponentTitle
                text: "↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑"
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 12
                horizontalAlignment: Text.AlignHCenter
            }
            Button {
                text: "▶"
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: function(){
                    var coord = positionSrc.position.coordinate;
                    menuComponentTitle.text = coord.longitude + " - " + coord.latitude
                }
            }
        }
    }

    PositionSource {
        id: positionSrc
        updateInterval: 3000
        //nmeaSource: "149.nmea"
        active: true

        onPositionChanged: {
            var coord = positionSrc.position.coordinate;
            console.log("Coordinate:", coord.longitude, coord.latitude);
            appWindow.title = "Coordinate:" + coord.longitude + "   " + coord.latitude
        }
    }
}
