# threading-ownership — 事件循环、线程亲和与对象所有权

## 判据要点

- **线程亲和（thread affinity）**：每个 `QObject` 属于一个线程，由其创建时的线程决定；
  只能在所属线程操作。跨线程操作 = 数据竞争，须 `moveToThread()` 且对象**无 parent**。
- `moveToThread` 之后，该对象的定时器、queued 连接、事件处理都跟着走；但已创建的
  `QTimer` 若 parent 是主线程对象，仍在主线程触发——这是最常见的「定时器跑错线程」。
- GUI 铁律：`QWidget`/`QQuickItem` 及其动画只能在 GUI 线程创建、访问、销毁。
  工作线程要更新 UI，只允许 queued 信号或 `QMetaObject::invokeMethod(..., Qt::QueuedConnection)`。
- 所有权两轨制：**parent 树**（`QObject` 层次，`deleteLater` 安全）与**智能指针**
  （`QScopedPointer`/`std::unique_ptr`）。混用即双删：给 `QObject` 套 `shared_ptr` 再设 parent，
  两边都会 delete。Qt6 有 `std::unique_ptr` 特化 `QObjectDelete` 可用，但仍不得与 parent 并存。
- `deleteLater()` 只是投递 `DeferredDelete` 事件，须回到该线程事件循环才真删；
  线程退出前须显式处理（`QThread::quit()` + `wait()`，或 `sendPostedEvents(nullptr, QEvent::DeferredDelete)`）。
- `QPointer` 持弱引用，对象销毁后自动置空——用于「可能先于我死掉的 QObject」；
  `QWeakPointer` 只配 `QSharedPointer` 用，别和 parent 树混。
- 事件循环：`QCoreApplication::exec()` 是 GUI 线程心跳；在槽里做阻塞 IO = 冻结界面。
  长任务改 `QThreadPool`/`QtConcurrent` 或 worker `QThread`。
- 同步原语：`QMutex`/`QReadWriteLock` 只护数据，不护对象；跨线程共享 `QObject` 指针本身
  就是竞争。锁粒度判据转派 `concurrency-design`。
- PyQt/PySide 注记：Python 引用会延长包装对象生命周期，C++ 侧已删而 Python 侧仍持有 →
  「Internal C++ object already deleted」；须靠 parent 或 `sip.delete()`/显式 del。

## 取证

`python -B scripts/env_probe.py --dir <proj>`；`QThread::currentThread() == obj->thread()` 打点；
TSan 构建（`-fsanitize=thread`）实跑一次才算「无数据竞争」。

## 边界

只出 Qt 线程模型级取证；并发架构（线程池规模、无锁结构）转派 `concurrency-design`。
