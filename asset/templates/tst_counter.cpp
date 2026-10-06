// tst_counter.cpp — Qt Test 骨架（含跨线程信号的正确等待方式）
// 判据：queued 信号不得立即断言，须 QSignalSpy::wait 或 QTRY_VERIFY。
#include <QtTest>
#include <QSignalSpy>

#include "counter.h"

class TstCounter : public QObject {
    Q_OBJECT

private slots:
    void initTestCase_data() {                 // 数据驱动
        QTest::addColumn<int>("start");
        QTest::newRow("zero") << 0;
        QTest::newRow("ten") << 10;
    }

    void increments() {
        QFETCH(int, start);
        Counter counter;
        QSignalSpy spy(&counter, &Counter::valueChanged);
        for (int i = 0; i < 3; ++i) {
            counter.increment();
        }
        QCOMPARE(counter.value(), start + 3);
        QCOMPARE(spy.count(), 3);              // 通知次数即契约
    }

    void sameValueNoNotify() {
        Counter counter;
        QSignalSpy spy(&counter, &Counter::valueChanged);
        counter.increment();
        counter.increment();                   // 同值第二次不应发通知
        QCOMPARE(spy.count(), 1);
    }
};

QTEST_GUILESS_MAIN(TstCounter)
#include "tst_counter.moc"                       // Q_OBJECT 在 .cpp：须让构建系统对其跑 moc
