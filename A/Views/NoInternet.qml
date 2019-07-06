import QtQuick 2.4

NoInternetForm {

    retryButton.onClicked: {
        stackView.pop()
    }
}
