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
                text: "..."
                anchors.horizontalCenter: parent.horizontalCenter
                font.pointSize: 12
                horizontalAlignment: Text.AlignHCenter
            }
            Button {
                text: "▶"
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: function(){
                    var coord = positionSrc.position.coordinate;
                    var txt = coord.longitude + " - " + coord.latitude + "\n";
                    txt += "longitude: " + coord.longitude.longitude + "(" + positionSrc.position.longitudeValid + ")\n"
                    txt += "latitude: " + coord.latitude + "(" + positionSrc.position.latitudeValid + ")\n"
                    txt += "altitude: " + coord.altitude + "(" + positionSrc.position.altitudeValid + ")\n"
                    txt += "direction: " + positionSrc.position.direction + "(" + positionSrc.position.directionValid + ")\n"
                    txt += "horizontalAccuracy: " + positionSrc.position.horizontalAccuracy + "(" + positionSrc.position.horizontalAccuracyValid + ")\n"
                    txt += "magneticVariation: " + positionSrc.position.magneticVariation + "(" + positionSrc.position.magneticVariationValid + ")\n"
                    txt += "speed: " + positionSrc.position.speed + "(" + positionSrc.position.speedValid + ")\n"
                    txt += "verticalAccuracy: " + positionSrc.position.verticalAccuracy + "(" + positionSrc.position.verticalAccuracyValid + ")\n"
                    txt += "verticalSpeed: " + positionSrc.position.verticalSpeed + "(" + positionSrc.position.verticalSpeedValid + ")\n"
                    txt += "timestamp: " + positionSrc.position.timestamp
                    menuComponentTitle.text = txt;
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
