from __future__ import annotations
import time
from pathlib import Path


INPUT_DIR = Path("./process/parsed")
OUTPUT = Path("./process/merged/adblock.txt")


class DomainTree:
    """ Define domaintree """
    class Node:
        EMPTY: int = 0
        EXACT: int = 1
        SUFFIX: int = 2
        children: dict[str, Node]
        flag: int
        __slots__ = ("children", "flag")

        def __init__(self) -> None:
            self.children = {}
            self.flag = DomainTree.Node.EMPTY

    def __init__(self) -> None:
        self.root = self.Node()

    def insert(self, rules: set[str]) -> None:
        for rule in rules:
            node = self.root

            # Detect type
            if rule.startswith("+."):
                domain = rule[2:]
                flag = self.Node.SUFFIX
            else:
                domain = rule
                flag = self.Node.EXACT

            for label in reversed(domain.split(".")):
                # Break when suffix rules exists
                if node.flag == self.Node.SUFFIX:
                    break

                # Enter child node
                if label not in node.children:
                    node.children[label] = self.Node()
                node = node.children[label]

            # Cover
            else:
                if node.flag == self.Node.SUFFIX:
                    continue

                if flag == self.Node.SUFFIX:
                    node.children.clear()
                node.flag = flag

    def export(self) -> set[str]:
        rules = set()
        path = []

        def dfs(node) -> None:
            # End
            if node.flag == self.Node.EXACT:
                rules.add(
                    ".".join(reversed(path))
                )
            elif node.flag == self.Node.SUFFIX:
                rules.add(
                    "+." + ".".join(reversed(path))
                )
                return

            # Enter child node
            for label, child in node.children.items():
                path.append(label)
                dfs(child)
                path.pop()

        dfs(self.root)
        return rules


def load(path: Path) -> set[str]:
    rules = set()

    with path.open(
        encoding="utf-8"
    ) as file:
        for rule in file:
            rule = rule.strip()
            if rule:
                rules.add(rule)

    return rules


def main() -> None:
    domains = DomainTree()
    # Timer starts.
    start_time = time.time()

    # Creat domaintree
    for path in INPUT_DIR.glob("*.txt"):
        print(
            f"Loading: {path}"
        )
        domains.insert(load(path))

    # Save rules
    rules = domains.export()
    OUTPUT.parent.mkdir(
        exist_ok=True
    )
    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        for rule in sorted(rules):
            f.write(f"{rule}\n")
    print(
        f"Total rules: {len(rules)}"
    )

    # Timer stops.
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()