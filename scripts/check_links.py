"""check_links.py — 悬空链接校验：扫描 .md 相对链接，目标不存在即报悬空（红线：悬空=0）。"""
import os
import re
import sys

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP = (".git", "tmp", "__pycache__", "build")


def scan(root):
    bad = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            for target in iter_links(path):
                full = os.path.normpath(os.path.join(dirpath, target))
                if not os.path.exists(full):
                    bad.append((path, target))
    return bad


def iter_links(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print("读取失败:", path, exc)
        return
    for match in LINK.finditer(text):
        target = match.group(1).split("#")[0].strip()
        if not target or target.startswith(("http:", "https:", "mailto:", "local:")):
            continue
        yield target


def main(argv):
    root = argv[argv.index("--root") + 1] if "--root" in argv else "."
    bad = scan(root)
    for path, target in bad:
        print("悬空:", os.path.relpath(path, root), "->", target)
    print("悬空链接数 =", len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
