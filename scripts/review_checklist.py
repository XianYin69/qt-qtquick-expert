"""review_checklist.py — 输出指定叶（或全部）的评审清单，按 blocking/major/minor 分级计数。"""
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")
LEVELS = ("blocking", "major", "minor", "verify")


def load_leaves():
    try:
        return json.load(open(TREE, encoding="utf-8")).get("leaves", [])
    except OSError as exc:
        print("知识树不可读:", exc)
        return []
    except json.JSONDecodeError as exc:
        print("知识树 JSON 非法:", exc)
        return []


def read_checklist(leaf):
    path = os.path.join(ROOT, "asset", "checklists", leaf["id"] + ".md")
    if not os.path.exists(path):
        print("清单缺失:", path)
        return []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print("清单不可读:", path, exc)
        return []
    return [line for line in text.splitlines() if line.strip().startswith("- [ ]")]


def report(leaf):
    lines = read_checklist(leaf)
    counts = {level: 0 for level in LEVELS}
    for line in lines:
        for level in LEVELS:
            if "| " + level + " |" in line or level + " |" in line:
                counts[level] += 1
                break
    print("## %s（%d 项）" % (leaf["id"], len(lines)))
    for line in lines:
        print(line)
    print("分级:", " ".join("%s=%d" % (k, v) for k, v in counts.items()))
    return counts


def main(argv):
    wanted = argv[argv.index("--leaf") + 1] if "--leaf" in argv else None
    total = {level: 0 for level in LEVELS}
    for leaf in load_leaves():
        if wanted and leaf["id"] != wanted:
            continue
        for level, count in report(leaf).items():
            total[level] += count
    print("合计:", " ".join("%s=%d" % (k, v) for k, v in total.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
