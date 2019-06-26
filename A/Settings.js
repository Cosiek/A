
const DEBUG = permanentSettings.getIsDebug();

const PROTOCOL = DEBUG ? "http" : "https";
// TODO: what is my domain?
const SERVER_DOMAIN = PROTOCOL + (DEBUG ? "://127.0.0.1:8080" : "TODO");
