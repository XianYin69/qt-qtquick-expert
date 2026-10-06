"""qml_lint.py — 优先调 qmllint；不可用时降级为静态疑点扫描（结论一律标 [本地]）。"""
import os
import re
import shutil
import subprocess
import sys

QML = (".qml", ".qs")
SUSPECT = [
    (re.compile(r"\bQt\.createObject\b"), "Qt.createObject 已弃用，改 Qt.createQmlObject/组件"),
    (re.compile(r"\bimport\s+QtQuick\.Controls\s+1\b"), "Controls 1.x 属 Qt5 遗留，Qt6 用 2.x"),
    (re.compile(r"\bon\s+Clicked\b"), "信号名大小写错误（clicked）"),
    (re.compile(r"\bproperty\s+var\s+\w+\s*:\s*null\b"), "var 属性无类型，QML 编译器无法静态检查"),
]


def run_qmllint(paths):
    exe = shutil.which("qmllint") or shutil.which("qmllint6")
    if not exe:
        return None
    try:
        proc = subprocess.run([exe, *paths], capture_output=True, text=True, timeout=60)
    except (subprocess.SubprocessError, OSError) as exc:
        print("qmllint 执行失败:", exc)
        return None
    print("qmllint rc=%d" % proc.returncode)
    for line in (proc.stdout + proc.stderr).splitlines():
        if line.strip():
            print("  ", line)
    return proc.returncode


def strip_comments(text):
    """去掉 // 与 # 行注释，避免注释里的术语被当成代码命中。"""
    out = []
    for line in text.splitlines():
        cut = line.find("//")
        if cut >= 0:
            line = line[:cut]
        if line.lstrip().startswith("#"):
            line = ""
        out.append(line)
    return "\n".join(out)


def static_scan(root):
    hits = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "build", "tmp")]
        for name in filenames:
            if not name.endswith(QML):
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError as exc:
                print("不可读:", path, exc)
                continue
            body = strip_comments(text)
            for pattern, note in SUSPECT:
                if pattern.search(body):
                    print(os.path.relpath(path, root), "|", note, "[本地]")
                    hits += 1
    return hits


def main(argv):
    root = argv[argv.index("--dir") + 1] if "--dir" in argv else os.getcwd()
    paths = [os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs if f.endswith(QML)]
    rc = run_qmllint(paths) if paths else None
    hits = static_scan(root)
    print("qmllint =", "未安装(降级)" if rc is None else "rc=%d" % rc, "| 静态疑点 =", hits)
    return 0 if rc is None else rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
