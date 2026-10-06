"""perf_probe.py — 渲染性能静态疑点：场景图友好性与常见 QML 卡顿模式。"""
import os
import re
import sys

PATTERNS = [
    (re.compile(r"\bLayer\.effect\b"), "layer.effect 强制离屏渲染，代价高"),
    (re.compile(r"\bGradient\b"), "Gradient 每帧重建，量大时改贴图"),
    (re.compile(r"\bvisible:\s*index\s*[<>]"), "delegate 仅切 visible 不销毁，内存仍占"),
    (re.compile(r"\bRepeater\b"), "Repeater 全量实例化，大列表改 ListView + delegate"),
    (re.compile(r"\bonPaint\b|\bonPaint\("), "自定义 paint：确认未每帧新建 QPainter/QPen"),
    (re.compile(r"\bTimer\s*\{[^}]*interval:\s*0\b", re.S), "interval=0 的 Timer 会占满事件循环"),
    (re.compile(r"\bQt\.Quick\.Window\b.*\bcolor:\s*\"transparent\""), "透明窗口禁用部分合成优化"),
    (re.compile(r"\banchors\.fill:\s*parent\b[\s\S]{0,80}\bMouseArea\b"), "全屏 MouseArea 遮挡下层命中测试"),
]
SRC = (".qml", ".qs")


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
                print(os.path.relpath(path, root), "|", note, "[本地]")
                total += 1
    print("性能疑点 =", total)
    print("须实测：QML Profiler / scene graph 后端（opengl | threaded | software）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
