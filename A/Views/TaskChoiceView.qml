import QtQuick 2.4
import QtQuick.Controls 2.1

import "../HttpRequest.js" as HttpRequest
import "../Messages.js" as Messages

TaskChoiceViewForm {

    function getLines(){
        lockForm()

        // prepare success callback
        function success(xhr){
            var resp = JSON.parse(xhr.responseText);
            // fill lines combo box with options
            lineChoice.model.clear()
            for (var idx in resp.list){
                var l = resp.list[idx]
                lineChoice.model.append(
                            {text: l.name, id: l.id })
            }
            // fill with prefered line data
            var line = resp.preferredLine || permanentSettings.get('lastLine') || ""
            if (lineChoice.find(line) !== -1){
                lineChoice.currentIndex = lineChoice.find(line)
                // get brigades for selected line
                getBrigades()
            } else {
                var txt = lineChoice.currentText.length ? "Nieznana linia" : ""
                unlockForm(txt)
            }
        }

        // prepare fial callback - not really worth doeing much about it.
        function fial(xhr){ unlockForm() }

        // send request
        HttpRequest.send("/lines", {}, success, fial)
    }

    function getBrigades(){
        lockForm()

        // prepare success callback
        function success(xhr){
            var resp = JSON.parse(xhr.responseText);
            // fill brigades combo box with options
            brigadeChoice.model.clear()
            for (var idx in resp.list){
                var b = resp.list[idx]
                brigadeChoice.model.append({text: b.name, id: b.id })
            }
            // fill with prefered line data
            var brigade = (resp.preferedBrigade ||
                           permanentSettings.get('lastBrigade') || "")
            if (brigadeChoice.find(brigade) !== -1){
                brigadeChoice.currentIndex = brigadeChoice.find(brigade)
            }

            unlockForm()
        }

        // prepare fial callback - not really worth doeing much about it.
        function fial(xhr){ unlockForm() }

        // prepare package
        var item = lineChoice.model.get(lineChoice.currentIndex)
        var pack = { lineId: item.id }

        // send request
        HttpRequest.send("/line/brigades", pack, success, fial)
    }

    function logout(){
        lockForm()
        // prepare callbacks
        function success(xhr){
            unlockForm()
            // jump to login view
            stackView.pop()
        }
        function fial(xhr){
            var txt = xhr.status + ": " + xhr.statusText
            unlockForm(txt  + " - " + xhr.responseText)
        }
        // send request to server
        HttpRequest.send("/driver/logout", {}, success, fial)
    }

    function chooseTask(){
        lockForm()
        // prepare callbacks
        function success(xhr){
            unlockForm()
            // save choice
            var line = lineChoice.model.get(lineChoice.currentIndex)
            var brigade = brigadeChoice.model.get(brigadeChoice.currentIndex)
            permanentSettings.set('lastLine', line.text)
            permanentSettings.set('lastBrigade', brigade.text)
            // TODO: jump to task view
        }
        function fial(xhr){
            var txt = Messages.get('error_server_response') + "\n"
            txt += xhr.status + ": " + xhr.statusText
            if (xhr.status + ": " + xhr.statusText !== xhr.responseText){
                txt += "\n" + xhr.responseText
            }
            unlockForm(txt)
        }

        // data prepare package
        var pack = {
            'line': lineChoice.model.get(lineChoice.currentIndex).id,
            'brigade': brigadeChoice.model.get(brigadeChoice.currentIndex).id
        }

        // send request to server  // TODO: rethink urls
        HttpRequest.send("/driver/start_task", pack, success, fial)
    }

    function techDriveChoice(){
        lockForm()
        // prepare callbacks
        function success(xhr){
            unlockForm()
            // TODO: jump to task view
        }
        function fial(xhr){
            var txt = Messages.get('error_server_response') + "\n"
            txt += xhr.status + ": " + xhr.statusText
            if (xhr.status + ": " + xhr.statusText !== xhr.responseText){
                txt += "\n" + xhr.responseText
            }
            unlockForm(txt)
        }

        // send request to server
        HttpRequest.send("/driver/tech_drive", {}, success, fial)
    }

    function lockForm(){
        setFormActive(false)
        requestErrorText.text = ''
    }

    function unlockForm(requestErrorTextText){
        setFormActive(true)
        requestErrorText.text = requestErrorTextText || ''
    }

    function setFormActive(isActive){
        busyIndicator.running = !isActive
        lineChoice.enabled = isActive
        brigadeChoice.enabled = isActive
        confirmButton.enabled = isActive
        logoutButton.enabled = isActive
    }

    lineChoice.onCurrentIndexChanged: getBrigades()

    logoutButton.onClicked: logout()

    confirmButton.onClicked: chooseTask()

    techDriveButton.onClicked: techDriveChoice()

    StackView.onActivating: getLines()
}
