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
                form.unlockForm()
                var resp = JSON.parse(xhr.responseText);
                // fill login with prefered driver data
                // TODO: lastDriver from permanentSettings
                // TODO: server can send "sugested" driver
                loginNameInput.textRole = resp.lastDriver || ""
                // check if password is required
                if (!resp.passwordRequired){
                    loginPasswordInput.text = ""
                    loginPasswordInput.enabled = false
                }
                // fill combo box with options
                for (var idx in resp.list){
                    loginNameInput.model.append({ text: resp.list[idx].name })
                }
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
        // send request to server
        HttpRequest.send(
                    "https://postman-echo.com/get",
                    {},
                    function(xhr){console.log(":D " + xhr.status)},
                    function(xhr){console.log(":,( " + xhr.status)}
        )

        DB.writeLoginDataToDB(login, pass)
        var msg = "???"
        form.unlockForm(msg)
    }

    loginButton.onClicked: {
        // set view attributes
        form.logIn(loginNameInput.text, loginPasswordInput.text)
    }

    registrationViewLink.onClicked: {
        stackView.push("DeviceRegView.qml")
    }

    StackView.onActivating: enterForm()

    Component.onCompleted: enterForm()
}
