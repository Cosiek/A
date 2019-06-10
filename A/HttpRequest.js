
function send(url, data, success, fial){
    // get id and key
    var id = ""
    var key = ""
    // make the request
    send(url, data, id, key, success, fial)
}


function _send(url, data, id, key, success, fial){
    // sign data
    data['id'] = id
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
        } else if (xhr.readyState === XMLHttpRequest.DONE
                   && xhr.status === 0){
            fial(xhr)
        }
    })
    xhr.onerror = fial

    xhr.open('POST', url, true);
    xhr.send(data);
}
