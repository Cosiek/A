import QtQuick 2.4
import QtQuick.Controls 2.1

import "../HttpRequest.js" as HttpRequest
import "../Messages.js" as Messages

DeviceRegViewForm {

    StackView.onActivating: {
        idInput.text = permanentSettings.get('identifier') || ''
    }

    backButton.onClicked: {
        stackView.pop()
    }

    saveButton.onClicked: {
        lockForm()

        // define callbacks
        function success(xhr){
            busyIndicator.running = false
            // save registration data
            permanentSettings.set('identifier', idInput.text)
            permanentSettings.set('key', keyInput.text)
            stackView.pop()
        }

        function fial(xhr){
            // display error msg
            var txt = Messages.get('error_server_response') + '\n'
            txt += xhr.status + ": " + xhr.statusText
            if (xhr.status + ": " + xhr.statusText !== xhr.responseText){
                txt += "\n" + xhr.responseText
            }
            errorText.text = txt

            unlockForm()
        }

        // prepare data to send
        var dt = { 'id': idInput.text }
        // make a request
        HttpRequest._send("/device/register", dt, dt.id, keyInput.text,
                          success, fial)
    }

    function lockForm(){
        busyIndicator.running = true
        saveButton.enabled = false
        backButton.enabled = false
        keyInput.enabled = false
        idInput.enabled = false
    }

    function unlockForm(){
        busyIndicator.running = false
        saveButton.enabled = true
        backButton.enabled = true
        keyInput.enabled = true
        idInput.enabled = true
    }
}
