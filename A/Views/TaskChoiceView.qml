import QtQuick 2.4

TaskChoiceViewForm {

    logoutButton.onClicked: {
        console.log("Uciekam!")
        stackView.pop()
    }
}
