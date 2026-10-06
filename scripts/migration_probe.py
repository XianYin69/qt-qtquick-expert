"""migration_probe.py — Qt5→Qt6 迁移疑点扫描（端口指南为准，条目须可复现验证）。"""
import os
import re
import sys

PATTERNS = [
    (re.compile(r"\bQRegExp\b"), "QRegExp 已移除，改 QRegularExpression"),
    (re.compile(r"\bQStringRef\b"), "QStringRef 已移除，改 QStringView"),
    (re.compile(r"\bQTextCodec\b"), "QTextCodec 移出 Qt Core，改 QIconvCodecConverter/ICU"),
    (re.compile(r"\bQt::Alignment\b(?!\s*=)"), "Qt::Alignment 改 Qt::AlignmentFlag"),
    (re.compile(r"\bQVariant\(\)\.type\(\)"), "QVariant::type() 移除，改 QVariant::typeId()"),
    (re.compile(r"\bQDesktopWidget\b"), "QDesktopWidget 移除，改 QScreen/QGuiApplication::screens()"),
    (re.compile(r"\bQRegExpValidator\b"), "QRegExpValidator 移除，改 QRegularExpressionValidator"),
    (re.compile(r"\bQT += quickcontrols2\b"), "Qt6 中 quickcontrols2 已并入 quick"),
    (re.compile(r"\bQVector\b"), "Qt6 QVector=std::vector 别名：注意与 QList 语义合并"),
    (re.compile(r"\bhighDpiScaleFactorRoundingPolicy\b"), "高 DPI 取整策略需显式设置（Qt6 默认变化）"),
    (re.compile(r"\bQMAKE_CXXFLAGS\b"), "qmake 遗留变量：Qt6 建议迁 CMake"),
]
SRC = (".h", ".hpp", ".cpp", ".cc", ".qml", ".pro", ".cmake", ".txt")


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


def scan(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print("不可读:", path, exc)
        return []
    body = strip_comments(text)
    return [note for pattern, note in PATTERNS if pattern.search(body)]


def main(argv):
    root = argv[argv.index("--dir") + 1] if "--dir" in argv else os.getcwd()
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "build", "tmp")]
        for name in filenames:
            if not name.endswith(SRC):
                continue
            path = os.path.join(dirpath, name)
            for note in scan(path):
                print(os.path.relpath(path, root), "|", note)
                total += 1
    print("迁移疑点 =", total)
    print("判据出处：doc.qt.io/qt-6/portingguide.html [联网]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
