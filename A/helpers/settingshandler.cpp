#include "settingshandler.h"

SettingsHandler::SettingsHandler(QObject *parent) : QObject(parent)
{
    QSettings t("Cosiek Inc.", "A");
}

void SettingsHandler::set(QString key, QVariant val){
    this->t.setValue(key, val);
}

QVariant SettingsHandler::get(QString key){
    return this->t.value(key);
}
