Qt.include("Settings.js")

function send(url, data, success, fial){
    // get id and key
    var id = permanentSettings.get('identifier');
    var key = permanentSettings.get('key');
    // make the request
    _send(url, data, id, key, success, fial)
}


function _send(url, data, id, key, success, fial){
    // sign data
    data['id'] = id
    data['timestamp'] = Date.now()
    data['signature'] = getSignature(data, key)
    // send request
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = (function() {
        if (xhr.readyState === XMLHttpRequest.DONE
                && xhr.status === 200) {
            success(xhr)
        } else if (xhr.readyState === XMLHttpRequest.DONE
                && xhr.status === 0){
            console.log("TODO: No internet connection!")
            fial(xhr)
        } else if (xhr.readyState === XMLHttpRequest.DONE){
            fial(xhr)
        }
    })
    xhr.onerror = fial

    // prepare url
    if (url.indexOf("http") !== 0){
        url = SERVER_DOMAIN + url;
    }

    xhr.open('POST', url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(data));
}


function getSignature(data, key){
    return signer.getSignature(JSON.stringify(data), key)
}
