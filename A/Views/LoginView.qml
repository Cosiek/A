import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.LocalStorage 2.0

import "../DBHandling.js" as DB
import "../HttpRequest.js" as HttpRequest
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

            // prepare fial callback (not really worth doeing anything about
            // missing drivers list)
            // MAYBE: check if it is a 403 and open device registration?
            // TODO: This is a good place to check for internet connection
            function fial(xhr){ unlockForm(txt) }

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
        return signer.obscure(password, permanentSettings.get('key'))
    }

    function logIn(login, pass){
        // TODO: use some file for text messages
        var MESSAGES = {
            'login_required': "Login jest wymagany",
            'password_required': "Hasło jest wymagane",
        }
        form.lockForm()
        // validate passed data
        var validationMessage = ""
        if (!login){ validationMessage += MESSAGES.login_required + "\n" }
        if (!pass){ validationMessage += MESSAGES.password_required }
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
            console.log(":,( " + xhr.status)
            var msg = "???"
            form.unlockForm(msg)
        }

        //prepare data package
        var pack = { 'login': login, 'pass': pass }

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
