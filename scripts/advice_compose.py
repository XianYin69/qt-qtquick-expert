"""advice_compose.py — 把叶判定组装为交付文本（结论/依据/取证/边界/未覆盖 五段缺一不可）。"""
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")
SECTIONS = ("结论", "依据", "取证", "边界", "未覆盖")
PLACEHOLDER = "<"


def leaf_ids():
    try:
        data = json.load(open(TREE, encoding="utf-8"))
    except OSError as exc:
        print("知识树不可读:", exc)
        return []
    except json.JSONDecodeError as exc:
        print("知识树 JSON 非法:", exc)
        return []
    return [leaf["id"] for leaf in data.get("leaves", [])]


def parse(argv, flag):
    if flag in argv:
        idx = argv.index(flag)
        if idx + 1 < len(argv):
            return argv[idx + 1].strip()
    return ""


def filled(value):
    """占位符（以 < 开头）视为未填，不得冒充已取证。"""
    return bool(value) and not value.startswith(PLACEHOLDER)


def main(argv):
    leaf = parse(argv, "--leaf")
    if leaf and leaf not in leaf_ids():
        print("未知叶:", leaf, "可用:", ",".join(leaf_ids()))
        return 2
    body = {
        "结论": parse(argv, "--verdict") or "<待填：一句话可执行判断>",
        "依据": parse(argv, "--basis") or "<官方文档条文/标准条款/实测输出>",
        "取证": parse(argv, "--evidence") or "<可复现命令：moc/qmllint/cmake --build/实测>",
        "边界": parse(argv, "--scope") or "<Qt6 版本区间；Widgets/Quick/绑定 哪一侧不适用>",
        "未覆盖": parse(argv, "--gaps") or "<未验证项与需转派的专项技能>",
    }
    if leaf:
        print("# 交付 · %s" % leaf)
    for name in SECTIONS:
        print("%s: %s" % (name, body[name]))
    empty = [name for name in SECTIONS if not filled(body[name])]
    if empty:
        print("缺段:", ",".join(empty), "→ 判不合格（红线：交付必含边界与未覆盖）")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
