import QtQuick 2.10
import QtQuick.Controls 2.1
import QtQuick.Window 2.10
import QtPositioning 5.10

import "Views"


Window {
    id: appWindow
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: "Views/LoginView.qml"
    }



    /*

    PositionSource {
        id: positionSrc
        updateInterval: 3000
        //nmeaSource: "149.nmea"
        active: false

        onPositionChanged: {
            console.log("XXX", positionSrc.active, positionSrc.updateInterval)
            var coord = positionSrc.position.coordinate;

            var jsonString = JSON.stringify(positionSrc.position);
            console.log(jsonString)

            var txt = "Position\n";
            txt += "longitude: " + coord.longitude + " (" + positionSrc.position.longitudeValid + ")\n"
            txt += "latitude: " + coord.latitude + " (" + positionSrc.position.latitudeValid + ")\n"
            txt += "altitude: " + coord.altitude + " (" + positionSrc.position.altitudeValid + ")\n"
            txt += "direction: " + positionSrc.position.direction + " (" + positionSrc.position.directionValid + ")\n"
            txt += "horizontalAccuracy: " + positionSrc.position.horizontalAccuracy + " (" + positionSrc.position.horizontalAccuracyValid + ")\n"
            txt += "magneticVariation: " + positionSrc.position.magneticVariation + " (" + positionSrc.position.magneticVariationValid + ")\n"
            txt += "speed: " + positionSrc.position.speed + " (" + positionSrc.position.speedValid + ")\n"
            txt += "verticalAccuracy: " + positionSrc.position.verticalAccuracy + " (" + positionSrc.position.verticalAccuracyValid + ")\n"
            txt += "verticalSpeed: " + positionSrc.position.verticalSpeed + " (" + positionSrc.position.verticalSpeedValid + ")\n"
            txt += "timestamp: " + positionSrc.position.timestamp;
            //menuComponentTitle.text = txt;
        }
    }
    */
}
