
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

function getLoginDataFromDB(){
    var ret = {"login": null}
    var db = getDBHandle()
    db.transaction(
        function(tx){
            // pull out login data
            var rs = tx.executeSql('SELECT * FROM settings WHERE key = "login"')
            for (var i = 0; i < rs.rows.length; i++) {
                ret.login = rs.rows.item(i).val
            }
        }
    )
    return ret
}


function writeLoginDataToDB(login){
    var db = getDBHandle()
    db.transaction(
        function(tx){
            tx.executeSql('INSERT INTO settings VALUES("login", ?)', [login,])
        }
    )
}
