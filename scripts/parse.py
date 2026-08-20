import ipaddress
from pathlib import Path


# 配置
INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./process/parsed")
BLOCK_IP = {
    "0.0.0.0",
    "127.0.0.1",
    "::",
    "::1"
  }
UNSUPPORTED_MODIFIER= (
    "badfilter",
    "denyallow",
    "script",
    "image",
    "css",
    "third-party",
    "popup")

# 创建文件夹
OUTPUT_DIR.mkdir(
    exist_ok=True
)


def detect_type(line):
    # 删除注释
    rule = line.strip()
    if (
        not rule
        or rule.startswith("#")
        or rule.startswith("!")):
        return None
    # 检测Adblock规则类型
    parts = rule.split()
    if len(parts) < 2:
        try:
            ipaddress.ip_address(parts[0])
        except ValueError:
            if (
                rule.startswith("||")
                or rule.startswith("|")
                or rule.startswith("/")
                or "$" in rule
                or "*" in rule
                ):
                return "ADBLOCK", rule
            return "DOMAIN", rule
        return None
    try:
        ipaddress.ip_address(parts[0])
    except ValueError:
        return None
    # 判断Hosts规则类型
    if parts[0] in BLOCK_IP:
        rule = parts[1]
        return "HOSTS", rule
    return None


def parse_adblock_rules(line):
    rule = line
    # 删除放行规则
    if rule.startswith("@@"):
        return None
    # 删除不支持的规则
    if "http://" in rule or "https://" in rule:
        return None
    if "$" in rule:
        modifiers = [
            modifier.split("=", 1)[0]
            for modifier in rule.split("$", 1)[1].split(",")
        ]
        if any(
            modifier in modifiers
            for modifier in UNSUPPORTED_MODIFIER
        ):
            return None
    rule = rule.split("$", 1)[0]
    if not rule:
        return None
    # 删除正则规则
    if rule.startswith("/") and rule.endswith("/"):
        return None
    # 处理域名规则
    rule = rule.lower()
    if "^" in rule:
        rule = rule.split("^", 1)[0]
    if "/" in rule:
        rule = rule.split("/", 1)[0]
    if rule.startswith("||"):
        rule = rule[2:]
        if "*" in rule:
            if "*" in rule[1:]:
                return None
            if  rule.startswith("*."):
                rule = "+" + rule[1:]
                return rule
            rule = "+." + rule[1:]
        return rule
    if rule.startswith("|"):
        if rule.endswith("|"):
            rule = rule[1: -1]
            return rule
        rule = rule[1:]
        return rule
    if "*" in rule:
        if "*" in rule[2:]:
            return None
        if  rule.startswith("*."):
            rule = "+" + rule[1:]
            return rule
        rule = "+." + rule[1:]
        return rule
    return rule


def parse_hosts_rules(line):
    rule = line.lower()
    return rule


def main():
    # 检测规则类型
    for input_file in INPUT_DIR.glob("*.txt"):
        rules = set()
        print(
            f"Parsing: {input_file}"
        )
        with input_file.open(
            encoding="utf-8"
        ) as file:
            for line in file:
                result = detect_type(line)
                if result is None:
                    continue
                rule_type, rule = result
                # 根据类型处理规则
                if rule_type == "ADBLOCK":
                    rule = parse_adblock_rules(rule)
                elif rule_type == "HOSTS":
                    rule = parse_hosts_rules(rule)
                elif rule_type == "DOMAIN":
                    pass
                else:
                    continue
                if rule is None:
                    continue
                rules.add(rule)
        # 输出信息
        print(
            f"Found {len(rules)} rules"
        )
        # 输出规则
        output_file = OUTPUT_DIR / (
            input_file.stem + ".txt"
        )
        output_file.parent.mkdir(
            exist_ok=True
        )
        with output_file.open(
            "w",
            encoding="utf-8"
        ) as f:
            for rule in sorted(rules):
                f.write(
                    f"{rule}\n"
                )


if __name__ == "__main__":
    main()