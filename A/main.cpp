#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "helpers/signer.h"
#include "helpers/settingshandler.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);


    QScopedPointer<Signer> signer_ptr(new Signer);
    Signer * signer = signer_ptr.data();
    engine.rootContext()->setContextProperty("signer", signer);

    QScopedPointer<SettingsHandler> settings_handler_ptr(new SettingsHandler);
    SettingsHandler * settings_handler = settings_handler_ptr.data();
    engine.rootContext()->setContextProperty(
                "permanentSettings", settings_handler);

    engine.load(url);
    return app.exec();
}
