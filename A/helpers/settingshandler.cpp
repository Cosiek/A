#include "settingshandler.h"

SettingsHandler::SettingsHandler(QObject *parent, bool isDebug)
    : QObject(parent)
{
    this->isDebug = isDebug;
    QSettings t("Cosiek Inc.", "A");
}

bool SettingsHandler::getIsDebug(){
    return this->isDebug;
}

void SettingsHandler::set(QString key, QVariant val){
    this->t.setValue(key, val);
}

QVariant SettingsHandler::get(QString key){
    return this->t.value(key);
}
