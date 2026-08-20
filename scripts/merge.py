from pathlib import Path


# 配置
INPUT_DIR = Path("./process/parsed")
OUTPUT = Path("./process/merged/adblock.txt")


# 创建文件夹
OUTPUT.parent.mkdir(
    exist_ok=True
)


def load_rules(path):
    rules = []
    with path.open(
        encoding="utf-8"
    ) as file:
        for line in file:
            if not line
            rules.append(line)
    return rules


def main():
    # 初始化
    domain_rules = set()
    domain_suffix_rules = set()
    rules = set()
    # 分类规则
    for path in INPUT_DIR.glob("*.txt"):
        print(
            f"Loading: {path}"
        )
        for rule in load_rules(path):
            if rule.startswith("+."):
                domain_suffix_rules.add(rule)
            else:
                domain_rules.add(rule)
    # 合并去重
    for domain_rule in domain_rules.copy():
        for domain_suffix_rule in domain_suffix_rules:
            suffix = domain_suffix_rule[2:]
            if domain_rule == suffix or domain_rule.endswith("." + suffix):
                domain_rules.remove(domain_rule)
                break
    rules.update(domain_rules, domain_suffix_rules)
    # 输出规则
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