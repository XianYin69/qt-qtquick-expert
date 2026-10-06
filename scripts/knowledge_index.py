"""knowledge_index.py — 知识树查询与依赖清单自检（deps.json 必附 source_url）。"""
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")
DEPS = os.path.join(ROOT, "dependence", "deps.json")
REQUIRED = ("name", "source_url", "license", "version", "install", "checked_at")


def read_json(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except OSError as exc:
        print("文件不可读:", path, exc)
        return None
    except json.JSONDecodeError as exc:
        print("JSON 非法:", path, exc)
        return None


def show_leaf(tree, leaf_id):
    for leaf in tree.get("leaves", []):
        if leaf["id"] == leaf_id:
            print("id:", leaf["id"])
            print("title:", leaf.get("title"))
            print("priority:", leaf.get("priority"))
            print("probes:", ",".join(leaf.get("probes", [])))
            print("cites:", "; ".join(leaf.get("cites", [])))
            for key in ("knowledge", "checklist"):
                if leaf.get(key):
                    print(key + ":", leaf[key])
            return 0
    print("未知叶:", leaf_id)
    return 1


def check_deps():
    data = read_json(DEPS)
    if data is None:
        return 1
    bad = 0
    for item in data.get("dependencies", []):
        missing = [k for k in REQUIRED if not item.get(k)]
        if missing:
            print("缺字段:", item.get("name", "?"), missing)
            bad += 1
        elif not str(item["source_url"]).startswith(("http://", "https://", "local://")):
            print("source_url 非原始链接:", item["name"], item["source_url"])
            bad += 1
    print("依赖条目 =", len(data.get("dependencies", [])), "不合格 =", bad)
    return 1 if bad else 0


def main(argv):
    if "--check-deps" in argv:
        return check_deps()
    if "--leaf" in argv:
        tree = read_json(TREE)
        return 1 if tree is None else show_leaf(tree, argv[argv.index("--leaf") + 1])
    tree = read_json(TREE)
    if tree is None:
        return 1
    for leaf in tree.get("leaves", []):
        print(leaf["id"], "|", leaf.get("priority"), "|", leaf.get("title"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
