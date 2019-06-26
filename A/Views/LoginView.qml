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
                console.log(":D " + xhr.status)
                form.unlockForm()
                var resp = JSON.parse(xhr.responseText);
                // fill login with prefered driver data
                loginNameInput.text = resp.lastDriver || ""
                // check if password is required
                if (!resp.passwordRequired){
                    loginPasswordInput.text = ""
                    loginPasswordInput.enabled = false
                }
            }

            // prepare fial callback
            function fial(xhr){
                console.log(":,( " + xhr.status)
                // display error msg
                var txt = "Błąd!\nOdpowiedź serwera:\n"
                txt += xhr.status + ": " + xhr.statusText
                if (xhr.status + ": " + xhr.statusText !== xhr.responseText){
                    txt += "\n" + xhr.responseText
                }
                unlockForm(txt)
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

    function obscure(pass){
        // TODO
        return pass
    }

    function logIn(login, pass, obscured){
        // TODO: use some file for text messages
        var MESSAGES = {
            'login_required': "Login jest wymagany",
            'password_required': "Hasło jest wymagane",
        }
        form.lockForm()
        // validate passed data
        var isValid = true
        if (!login){ loginErrorText.text = MESSAGES.login_required; isValid = false }
        if (!pass){ loginErrorText.text = MESSAGES.password_required; isValid = false }
        if (!isValid){ form.unlockForm(); return null }
        // obscure password
        if (!obscured){ pass = form.obscure(pass) }
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
        form.logIn(loginNameInput.text, loginPasswordInput.text, false)
    }

    registrationViewLink.onClicked: {
        stackView.push("DeviceRegView.qml")
    }

    StackView.onActivating: enterForm()

    Component.onCompleted: enterForm()
}
