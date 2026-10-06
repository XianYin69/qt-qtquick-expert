"""classify_topic.py — 按关键词把用户问题映射到知识树叶（九叶），输出候选叶与命中词。"""
import json
import os
import sys

DEFAULT_TREE = os.path.join(os.path.dirname(__file__), "..", "asset", "knowledge_tree.json")


def load_tree(path):
    try:
        data = json.load(open(path, encoding="utf-8"))
    except OSError as exc:
        print("知识树不可读:", path, exc)
        return None
    except json.JSONDecodeError as exc:
        print("知识树 JSON 非法:", path, exc)
        return None
    return data


def score(text, leaf):
    lowered = text.lower()
    hits = [kw for kw in leaf.get("keywords", []) if kw.lower() in lowered]
    return len(hits), hits


def main(argv):
    tree_path = DEFAULT_TREE
    if "--tree" in argv:
        tree_path = argv[argv.index("--tree") + 1]
    query = " ".join(a for a in argv if not a.startswith("--"))
    if not query.strip():
        print("用法: classify_topic.py <问题文本> [--tree <path>]")
        return 2
    tree = load_tree(os.path.normpath(tree_path))
    if tree is None:
        return 1
    ranked = []
    for leaf in tree.get("leaves", []):
        count, hits = score(query, leaf)
        if count:
            ranked.append((count, leaf["id"], leaf.get("priority", 9), hits))
    ranked.sort(key=lambda item: (-item[0], item[2]))
    if not ranked:
        print("未命中任何叶 → 触发浏览器学习（resistance/浏览器学习约束）")
        return 3
    for count, leaf_id, priority, hits in ranked[:3]:
        print("%s\t分=%d\t优先级=%d\t命中=%s" % (leaf_id, count, priority, ",".join(hits[:6])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
