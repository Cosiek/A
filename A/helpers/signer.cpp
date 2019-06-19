#include <QJsonDocument>
#include <QJsonObject>
#include <QMessageAuthenticationCode>

#include "signer.h"

Signer::Signer(QObject *parent) : QObject(parent){
    this->algorithm = QCryptographicHash::Md5;
}


QString Signer::getSignature(QString dataJson, QString key)
{
    // unpack
    QJsonDocument jsonDocument(QJsonDocument::fromJson(dataJson.toUtf8()));
    QJsonObject ob = jsonDocument.object();
    // prepare data
    QString dt = "";
    QStringList keys = ob.keys();
    keys.sort();
    QString k;
    for (int i = 0; i < keys.size(); ++i){
        k = keys[i];
        if (ob.value(k).isString()){
            dt += k + ob.value(k).toString();
        } else if (ob.value(k).isDouble()) {
            dt += k + QString::number(ob.value(k).toDouble(), 'g', 15);
        }
    }
    // generate signature
    QMessageAuthenticationCode code(this->algorithm);
    code.setKey(key.toUtf8());
    code.addData(dt.toUtf8());
    return code.result().toHex();
}
