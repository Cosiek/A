import QtQuick 2.4
import QtQuick.LocalStorage 2.0

import "../DBHandling.js" as DB
import "../HttpRequest.js" as HttpRequest


LoginViewForm {
    id: form

    function lockForm() {
        loginNameInput.enabled = false
        loginPasswordInput.enabled = false
        loginButton.enabled = false
        loginErrorText.text = ' '
        busyIndicator.visible = true
    }

    function unlockForm(loginErrorTextText) {
        loginNameInput.enabled = true
        loginPasswordInput.enabled = true
        loginButton.enabled = true
        loginErrorText.text = loginErrorTextText || ' '
        busyIndicator.visible = false
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
                    null,
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

    Component.onCompleted: {
        // try to get login data from storage
        loginPasswordInput.echoMode = TextInput.PasswordEchoOnEdit
        // if login data is available...
        var logData = DB.getLoginDataFromDB(form.db)
        console.log(logData.login, logData.pass)

        if (logData.login && logData.pass){     // try to log in
            form.logIn(logData.login, logData.pass, true)
        } else {                                // otherwise unlock the form
            form.unlockForm()
        }
    }
}



/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
