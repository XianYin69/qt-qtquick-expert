"""deploy_probe.py — windeployqt/macdeployqt 干跑（--dry-run），并核对常见缺项。"""
import os
import re
import shutil
import subprocess
import sys

HINTS = [
    (re.compile(r"--no-translations", re.I), "跳过翻译部署：确认 qm 文件是否随包"),
    (re.compile(r"Qt6Quick|qtquick", re.I), "含 Quick：须部署 QML 插件与 qml/ 目录"),
    (re.compile(r"platforms", re.I), "平台插件目录已列出"),
]


def dry_run(target, extra):
    for name in ("windeployqt", "windeployqt6", "macdeployqt"):
        exe = shutil.which(name)
        if exe:
            break
    else:
        return None
    cmd = [exe, "--dry-run", *extra, target]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (subprocess.SubprocessError, OSError) as exc:
        print("干跑失败:", exc)
        return None
    out = proc.stdout + proc.stderr
    print("%s --dry-run rc=%d" % (name, proc.returncode))
    for line in out.splitlines():
        if line.strip():
            print("  ", line.strip())
    for pattern, note in HINTS:
        if pattern.search(out):
            print("  提示:", note)
    return proc.returncode


def main(argv):
    target = argv[argv.index("--target") + 1] if "--target" in argv else os.getcwd()
    extra = []
    if "--qml-dir" in argv:
        extra += ["--qmldir", argv[argv.index("--qml-dir") + 1]]
    rc = dry_run(target, extra)
    if rc is None:
        print("降级：部署工具不可用，只能给静态清单（标 [本地]）")
        print("静态清单：platforms/ styles/ imageformats/ tls/ qml/ *.dll|*.dylib translations/")
        return 3
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
