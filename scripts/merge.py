from pathlib import Path
import yaml


# 配置
INPUT_DIR = Path("./process/parsed")
OUTPUT = Path("./process/merged/adblock.yaml")



def load_rules(path):
    with path.open(
        encoding="utf-8"
    ) as f:
        data = yaml.safe_load(f) or {}
    return data.get(
        "payload",
        []
    )


def parse(line):
    if "," not in line:
        return None
    rule_type, value = line.split(",", 1)
    value = value.strip()
    if rule_type == "DOMAIN":
        pass
    elif rule_type == "DOMAIN-SUFFIX":
        value = "+." + value
    elif rule_type == "DOMAIN-WILDCARD":
        value = "+" + value[1:]
    else:
        return None
    return value


def main():
    # 初始化
    domain_rules = set()
    domain_suffix_rules = set()
    rules = set()
    OUTPUT.parent.mkdir(
        exist_ok=True
    )
    # 加载规则
    for file in INPUT_DIR.glob("*.yaml"):
        print(
            f"Loading: {file}"
        )
        for line in load_rules(file):
            value = parse(line)
            if value is None:
                continue
            elif value.startswith("+"):
                domain_suffix_rules.add(value)
            else:
                domain_rules.add(value)
    # 合并去重
    for a in domain_rules.copy():
        for b in domain_suffix_rules:
            suffix = b[2:]
            if a == suffix or a.endswith("." + suffix):
                domain_rules.remove(a)
                break
    rules.update(domain_rules, domain_suffix_rules)
    # 输出规则
    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        f.write("payload:\n")
        for rule in sorted(rules):
            f.write(f"  - {rule}\n")
    # 输出信息
    print(
        f"Total rules: {len(rules)}"
    )


if __name__ == "__main__":
    main()