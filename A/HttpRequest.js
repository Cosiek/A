
function send(url, data, success, fial){
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

    xhr.open('GET', url, true);
    xhr.send(data);
}
