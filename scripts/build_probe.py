"""build_probe.py — 探测构建方式：CMake（qt_add_qml_module）/ qmake 遗留 / 资源与依赖风险。"""
import os
import re
import sys

CMAKE_PATTERNS = [
    (re.compile(r"qt_add_qml_module\s*\("), "qt_add_qml_module 已声明"),
    (re.compile(r"find_package\s*\(\s*Qt5"), "混用 Qt5 包名（Qt6 项目应 find_package(Qt6)）"),
    (re.compile(r"qt5_add_resources|qt5_wrap_cpp"), "使用 Qt5 旧式资源/moc 包装函数"),
    (re.compile(r"target_link_libraries\s*\(\s*\w+\s+(PRIVATE|PUBLIC|INTERFACE)"), "链接可见性显式"),
    (re.compile(r"target_link_libraries\s*\(\s*\w+\s+(?!PRIVATE|PUBLIC|INTERFACE)"), "链接未写可见性关键字"),
    (re.compile(r"\bset\s*\(\s*CMAKE_AUTOMOC\s+OFF"), "AUTOMOC 关闭，须确认仍跑 moc"),
]
QMAKE_PATTERNS = [
    (re.compile(r"^\s*QT\s*\+=\s*quick\b", re.M), "QT += quick"),
    (re.compile(r"^\s*QT\s*\+=\s*quickcontrols2\b", re.M), "Qt5 遗留：quickcontrols2 在 Qt6 已并入 quick"),
    (re.compile(r"^\s*CONFIG\s*\+=\s*qt_quickcompiler", re.M), "QML 预编译已开启"),
]


def probe(path, patterns, label):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print("不可读:", path, exc)
        return 0
    hits = 0
    for pattern, note in patterns:
        if pattern.search(text):
            print("%s | %s | %s" % (label, os.path.basename(path), note))
            hits += 1
    return hits


def main(argv):
    root = argv[argv.index("--dir") + 1] if "--dir" in argv else os.getcwd()
    total = 0
    kinds = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "build", "tmp")]
        for name in filenames:
            path = os.path.join(dirpath, name)
            if name == "CMakeLists.txt":
                kinds.add("cmake")
                total += probe(path, CMAKE_PATTERNS, "CMake")
            elif name.endswith(".pro"):
                kinds.add("qmake")
                total += probe(path, QMAKE_PATTERNS, "qmake")
    print("构建系统 =", ",".join(sorted(kinds)) or "未发现", "| 疑点 =", total)
    if "cmake" in kinds and "qmake" in kinds:
        print("提示: 同一项目并存两套构建，须指明权威者")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
