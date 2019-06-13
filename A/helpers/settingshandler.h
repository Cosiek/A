#ifndef SETTINGSHANDLER_H
#define SETTINGSHANDLER_H

#include <QObject>
#include <QSettings>

class SettingsHandler : public QObject
{
    Q_OBJECT
public:
    explicit SettingsHandler(QObject *parent = nullptr, bool isDebug = false);

    Q_INVOKABLE void set(QString, QVariant);
    Q_INVOKABLE QVariant get(QString);
    Q_INVOKABLE bool getIsDebug();
private:
    bool isDebug;
    QSettings t;
signals:

public slots:
};

#endif // SETTINGSHANDLER_H
