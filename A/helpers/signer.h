#ifndef SIGNER_H
#define SIGNER_H

#include <QObject>
#include <QMessageAuthenticationCode>

class Signer : public QObject
{
    Q_OBJECT
public:
    explicit Signer(QObject *parent = nullptr);

    Q_INVOKABLE QString getSignature(QString, QString);
private:
    QCryptographicHash::Algorithm algorithm;
signals:

public slots:
};

#endif // SIGNER_H
