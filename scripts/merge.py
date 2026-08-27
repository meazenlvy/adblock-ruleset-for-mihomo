from pathlib import Path


# 配置
INPUT_DIR = Path("./process/parsed")
OUTPUT = Path("./process/merged/adblock.txt")


# 创建文件夹
OUTPUT.parent.mkdir(
    exist_ok=True
)


class DomainTree:
    class Node:
        EMPTY = 0
        EXACT = 1
        SUFFIX = 2

        __slots__ = ("children", "flag")

        def __init__(self):
            self.children = {}
            self.flag = DomainTree.Node.EMPTY

    def __init__(self):
        self.root = self.Node()

    def insert(self, rules):
        for rule in rules:
            node = self.root

            if rule.startswith("+."):
                domain = rule[2:]
                flag = self.Node.SUFFIX
            else:
                domain = rule
                flag = self.Node.EXACT

            for label in reversed(domain.split(".")):
                if node.flag == self.Node.SUFFIX:
                    break

                if label not in node.children:
                    node.children[label] = self.Node()
                node = node.children[label]
            else:
                if node.flag == self.Node.SUFFIX:
                    continue
                if flag == self.Node.SUFFIX:
                    node.children.clear()
                node.flag = flag

    def export(self):
        rules = set()
        path = []

        def dfs(node):
            if node.flag == self.Node.EXACT:
                rules.add(
                    ".".join(reversed(path))
                )
            elif node.flag == self.Node.SUFFIX:
                rules.add(
                    "+." + ".".join(reversed(path))
                )
                return

            # 遍历子节点
            for label, child in node.children.items():
                path.append(label)
                dfs(child)
                path.pop()

        dfs(self.root)

        return rules


def load(path):
    rules = set()

    with path.open(
        encoding="utf-8"
    ) as file:
        for rule in file:
            rule = rule.strip()
            if rule:
                rules.add(rule)

    return rules


def main():
    # 初始化
    domains = DomainTree()

    # 合并去重
    for path in INPUT_DIR.glob("*.txt"):
        print(
            f"Loading: {path}"
        )
        domains.insert(load(path))

    # 输出规则
    rules = domains.export()
    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        for rule in sorted(rules):
            f.write(f"{rule}\n")

    # 输出信息
    print(
        f"Total rules: {len(rules)}"
    )


if __name__ == "__main__":
    main()