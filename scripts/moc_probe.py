"""moc_probe.py — 静态检查 moc 前置：用了信号/槽/属性却缺 Q_OBJECT 的类。"""
import os
import re
import sys

SRC = (".h", ".hpp", ".cpp", ".cc")
CLASS = re.compile(r"\bclass\b[^\n{;]*\b([A-Z]\w*)\b[^\n]*[{;]")
NEED = re.compile(r"\b(signals|slots|Q_OBJECT|Q_PROPERTY|Q_ENUM|Q_INVOKABLE|emit)\b")


def scan_file(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print("不可读:", path, exc)
        return []
    issues = []
    has_macro = re.search(r"\bQ_OBJECT\b", text) is not None
    for match in CLASS.finditer(text):
        name = match.group(1)
        body = text[match.start():][:4000]
        if NEED.search(body) and not has_macro:
            issues.append("%s: 声明了信号/槽/属性但本文件无 Q_OBJECT（moc 不会生成元对象）" % name)
            break
    if has_macro and path.endswith((".cpp", ".cc")):
        issues.append("提示: Q_OBJECT 位于实现文件，确认构建系统对该 .cpp 也跑 moc")
    return issues


def main(argv):
    root = argv[argv.index("--dir") + 1] if "--dir" in argv else os.getcwd()
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "build", "tmp", "__pycache__")]
        for name in filenames:
            if not name.endswith(SRC):
                continue
            path = os.path.join(dirpath, name)
            for issue in scan_file(path):
                print(os.path.relpath(path, root), "|", issue)
                total += 1
    print("moc 相关疑点 =", total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
