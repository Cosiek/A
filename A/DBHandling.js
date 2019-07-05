
function getDBHandle(){
    return LocalStorage.openDatabaseSync("A_DB", "1.0", "A database", 1000000)
}


function dbInit(){
    var db = getDBHandle()
    db.transaction(function (tx) {
        // Create a table if it doesn't already exist
        tx.executeSql('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, val TEXT)')
    })
}

/* ============================================================================
LOGIN
============================================================================ */

function getLogin(){
    var login = null
    var db = getDBHandle()
    db.transaction(
        function(tx){
            // pull out login data
            var rs = tx.executeSql('SELECT * FROM settings WHERE key = "login"')
            for (var i = 0; i < rs.rows.length; i++) {
                login = rs.rows.item(i).val
            }
        }
    )
    return login
}


function writeLoginDataToDB(login){
    var db = getDBHandle()
    db.transaction(
        function(tx){
            tx.executeSql('INSERT INTO settings VALUES("login", ?)', [login,])
        }
    )
}
