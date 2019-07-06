
const DEBUG = permanentSettings.getIsDebug();

const PROTOCOL = DEBUG ? "http" : "https";
// TODO: what is my domain?
const SERVER_DOMAIN = PROTOCOL + (DEBUG ? "://127.0.0.1:8080" : "TODO");

// TODO: keep this private
const OBSCURATION_KEY = '5l=k-ssi+j616nyd@*6e-2!qkz4+s&amp;7rc544*w(9+xho0&amp;l25b'
