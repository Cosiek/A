
const MESSAGES = {
    'pl': {
        'error_server_response': "Błąd!\nOdpowiedź serwera:",
        'is_device_registered': "Błąd zapytania do serwera.\nCzy urządzenie jest zarejestrowane?",
        'login_required': "Login jest wymagany",
        'password_required': "Hasło jest wymagane",
    }
}

function get(key) {
    var lng = permanentSettings.get('language') || 'pl'
    return MESSAGES[lng][key];
}
