import QtQuick 2.4

DeviceRegViewForm {

    backButton.onClicked: {
        stackView.pop()
    }

    saveButton.onClicked: {
        busyIndicator.running = !busyIndicator.running
    }
}
