#include <QMessageAuthenticationCode>

#include "signer.h"

Signer::Signer(QObject *parent) : QObject(parent)
{ }


QString Signer::getSignature(QString dataJson, QString key)
{
    QMessageAuthenticationCode code(QCryptographicHash::Sha1);
    code.setKey(key.toUtf8());
    code.addData(dataJson.toUtf8());
    return code.result().toHex();
}
