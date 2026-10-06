# 线程与所有权骨架（threading-ownership）

## worker 线程正确形态（判据摘要）

```cpp
class Worker : public QObject {
    Q_OBJECT
public:
    explicit Worker() {}                       // 关键：不传 parent
public slots:
    void run() { /* 耗时工作，不碰 UI */ emit done(result); }
signals:
    void done(int result);
};

auto *thread = new QThread(this);              // thread 有 parent，随主对象销毁
auto *worker = new Worker();                   // 无 parent，才能 moveToThread
worker->moveToThread(thread);
connect(worker, &Worker::done, this, &App::onDone);   // AutoConnection → Queued
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
thread->start();
// 退出：thread->quit(); thread->wait();  否则 deleteLater 永不兑现
```

## 反例（blocking）

| 反例 | 后果 |
|---|---|
| `new Worker(this)` 后 `moveToThread` | 亲和仍属主线程，槽在主线程跑 |
| GUI 线程槽里做阻塞 IO | 界面冻结 |
| `shared_ptr<QObject>` + 同时设 parent | 双删崩溃 |
| 工作线程直接 `label->setText()` | 数据竞争 / 未定义行为 |
| 用 `QTimer` 且 parent 在主线程 | 定时器在主线程触发 |

## 绑定层注记

PySide6/PyQt6：Python 引用会延长包装对象生命周期，C++ 侧已删而 Python 侧仍持有 →
「Internal C++ object already deleted」；靠 parent 或显式 del 解决。

## 出处

threads · signalsandslots（见 [参考书目](../../references/参考书目/参考书目.md)）
