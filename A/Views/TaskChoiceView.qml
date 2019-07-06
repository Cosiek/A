import QtQuick 2.4

import "../HttpRequest.js" as HttpRequest

TaskChoiceViewForm {

    logoutButton.onClicked: {
        console.log("Uciekam!")
        // TODO: lock form
        // prepare callbacks
        function success(xhr){
            console.log("Wylogowany! :)")
            // TODO: unlock form
            // jump to login view
            stackView.pop()
        }
        function fial(xhr){
            // TODO: unlock form
            var txt = xhr.status + ": " + xhr.statusText + " - " + xhr.responseText
            console.log("Nic nie boli tak jak życie! :/")
            console.log(txt)
        }
        // send request to server
        HttpRequest.send("/driver/logout", {}, success, fial)
    }
}
