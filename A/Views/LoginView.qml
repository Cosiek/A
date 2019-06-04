import QtQuick 2.4
import QtQuick.LocalStorage 2.0


LoginViewForm {
    id: form
    property var db: null

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

    function sendRequest(url, data, success, fial){
        // TODO - move this someplace else
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = (function() {
            if (xhr.readyState === XMLHttpRequest.DONE
                    && xhr.status === 200) {
                success(xhr)
            } else if (xhr.readyState === XMLHttpRequest.DONE
                    && xhr.status === 0){
                console.log("TODO: No internet connection!")
            }
        })
        xhr.onerror = fial

        xhr.open('GET', url, true);
        xhr.send("x=1&y=2");
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
        form.sendRequest(
                    "https://postman-echo.com/get",
                    null,
                    function(){console.log(":D")},
                    function(){console.log(":,(")}
        )

        form.writeLoginDataToDB(form.db, login, pass)
        var msg = "???"
        form.unlockForm(msg)
    }

    function getLoginDataFromDB(db){
        var ret = {"login": null, "pass": null}
        db.transaction(
            function(tx){
                // Create a table if it doesn't already exist
                tx.executeSql('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, val TEXT)')
                // pull out login data
                var rs = tx.executeSql('SELECT * FROM settings WHERE key = "login" OR key = "pass"')
                for (var i = 0; i < rs.rows.length; i++) {
                    var row = rs.rows.item(i)
                    if (row.key === "login"){ ret.login = row.val }
                    if (row.key === "pass"){ ret.pass = row.val }
                }
            }
        )
        return ret
    }

    function writeLoginDataToDB(db, login, pass){
        db.transaction(
            function(tx){
                tx.executeSql('INSERT INTO settings VALUES("login", ?)', [login,])
                tx.executeSql('INSERT INTO settings VALUES("pass", ?)', [pass,])
            }
        )
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
        form.db = LocalStorage.openDatabaseSync("A_DB", "1.0", "A database", 1000000)
        var logData = form.getLoginDataFromDB(form.db)
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
