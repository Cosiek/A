#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "helpers/signer.h"

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

    engine.load(url);
    return app.exec();
}
