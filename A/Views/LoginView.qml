import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.LocalStorage 2.0

import "../DBHandling.js" as DB
import "../HttpRequest.js" as HttpRequest
import "../Messages.js" as Messages
import "../Settings.js" as Settings


LoginViewForm {
    id: form

    function enterForm(){
        form.lockForm()
        //registrationViewLink.enabled = false
        // check if device is registered
        if (permanentSettings.get('identifier') && permanentSettings.get('key')){
            // try to get drivers from server

            // prepare success callback
            function success(xhr){
                var resp = JSON.parse(xhr.responseText);
                // check if password is required
                loginPasswordInput.text = ""
                loginPasswordInput.enabled = resp.passwordRequired
                // fill combo box with options
                loginNameInput.model.clear()
                for (var idx in resp.list){
                    loginNameInput.model.append({ text: resp.list[idx].name })
                }
                // fill login with prefered driver data
                // TODO: server can send "sugested" driver
                var login = resp.lastDriver || DB.getLogin() || ""
                if (loginNameInput.find(login) !== -1){
                    loginNameInput.currentIndex = loginNameInput.find(login)
                }

                form.unlockForm()
            }

            // prepare fial callback (not really worth doeing much about
            // missing drivers list)
            function fial(xhr){
                var msg = xhr.status === 401 ? Messages.get(
                                                   'is_device_registered') : ""
                unlockForm(msg)
            }

            // send request
            HttpRequest.send("/drivers", {}, success, fial)
        } else {
            // allow way to device registration view
            registrationViewLink.enabled = true
        }
    }

    function lockForm() {
        loginNameInput.enabled = false
        loginPasswordInput.enabled = false
        loginButton.enabled = false
        loginErrorText.text = ' '
        busyIndicator.running = true
    }

    function unlockForm(loginErrorTextText) {
        loginNameInput.enabled = true
        loginPasswordInput.enabled = true
        loginButton.enabled = true
        loginErrorText.text = loginErrorTextText || ' '
        busyIndicator.running = false
    }

    function obscure(password){
        return signer.obscure(password, Settings.OBSCURATION_KEY)
    }

    function logIn(login, pass){
        form.lockForm()
        // validate passed data
        var validationMessage = ""
        if (!login){ validationMessage += Messages.get('login_required') + "\n" }
        if (!pass){ validationMessage += Messages.get('password_required') }
        if (validationMessage.length){
            form.unlockForm(validationMessage.trim());
            return null;
        }
        // obscure password
        pass = form.obscure(pass)
        // prepare callback functions
        function success(xhr){
            console.log(":D " + xhr.status)
            DB.writeLoginDataToDB(login)
            // go to next view
        }

        function fial(xhr){
            var txt = Messages.get('error_server_response') + "\n"
            txt += xhr.status + ": " + xhr.statusText
            if (xhr.status + ": " + xhr.statusText !== xhr.responseText){
                txt += "\n" + xhr.responseText
            }
            form.unlockForm(txt)
        }

        //prepare data package
        var pack = { 'login': login, 'password': pass }

        // send request to server
        HttpRequest.send("/driver/login", pack, success, fial)
    }

    loginButton.onClicked: {
        // set view attributes
        form.logIn(loginNameInput.currentText, loginPasswordInput.text)
    }

    registrationViewLink.onClicked: {
        stackView.push("DeviceRegView.qml")
    }

    StackView.onActivating: enterForm()

    Component.onCompleted: enterForm()
}
