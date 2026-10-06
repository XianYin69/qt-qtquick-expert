// counter.h — QML_ELEMENT + 可绑定属性骨架（Qt 6 主口径）
// 判据：Q_PROPERTY 必须带 NOTIFY，否则 QML 绑定不刷新；setter 同值不发通知。
#pragma once

#include <QObject>
#include <QtQml/qqmlregistration.h>

class Counter : public QObject {
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged FINAL)
public:
    explicit Counter(QObject *parent = nullptr) : QObject(parent) {}  // parent 树负责所有权

    int value() const { return m_value; }

public slots:
    void increment() { setValue(m_value + 1); }

signals:
    void valueChanged(int value);

private:
    void setValue(int v) {
        if (v == m_value) {          // 同值不通知，避免绑定风暴
            return;
        }
        m_value = v;
        emit valueChanged(m_value);
    }

    int m_value = 0;
};

// Qt 5.15 遗留注记：无 QML_ELEMENT，须 qmlRegisterType<Counter>("Org.App", 1, 0, "Counter");
