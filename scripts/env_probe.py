"""env_probe.py — 探测 Qt 环境：qmake / CMake / qmllint / windeployqt / PySide6 / PyQt6。"""
import os
import shutil
import subprocess
import sys


def run(cmd):
    """返回 (exe 或 None, 首行输出, 返回码或 None)。"""
    exe = shutil.which(cmd[0])
    if not exe:
        return None, "absent", None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except (subprocess.SubprocessError, OSError) as exc:
        return exe, "error: %s" % exc, None
    out = (proc.stdout or proc.stderr).strip().splitlines()
    return exe, (out[0] if out else "no-output"), proc.returncode


def report(name, exe, info, rc):
    if exe is None or rc not in (0,):
        print("%-14s ABSENT\t%s" % (name, info))
        return 0
    print("%-14s FOUND\t%s" % (name, info))
    return 1


def probe_tool(name, cmd):
    return report(name, *run(cmd))


def probe_module(name, code):
    return report(name, *run([sys.executable, "-c", code]))


def main(argv):
    root = argv[argv.index("--dir") + 1] if "--dir" in argv else os.getcwd()
    print("工作目录:", root)
    found = 0
    found += probe_tool("qmake", ["qmake", "-query", "QT_VERSION"])
    found += probe_tool("qmake6", ["qmake6", "-query", "QT_VERSION"])
    found += probe_tool("cmake", ["cmake", "--version"])
    found += probe_tool("qmllint", ["qmllint", "--version"])
    found += probe_tool("windeployqt", ["windeployqt", "--version"])
    found += probe_tool("macdeployqt", ["macdeployqt", "--help"])
    found += probe_module("pyside6", "import PySide6;print(PySide6.__version__)")
    found += probe_module("pyqt6", "from PyQt6.QtCore import QT_VERSION_STR;print(QT_VERSION_STR)")
    print("可用工具数 =", found)
    if found == 0:
        print("降级：判据只能来自静态阅读，须标 [本地] 并给可复现取证命令")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
