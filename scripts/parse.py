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


def detect_type(line):
    # 删除注释
    value = line.strip()
    if (
        not value
        or value.startswith("#")
        or value.startswith("!")):
        return None
    # 检测Adblock规则类型
    parts = value.split()
    if len(parts) < 2:
        try:
            ipaddress.ip_address(parts[0])
        except ValueError:
            if (
                value.startswith("||")
                or value.startswith("|")
                or value.startswith("/")
                or "$" in value
                ):
                return "ADBLOCK", value
            return "DOMAIN", value
        return None
    try:
        ipaddress.ip_address(parts[0])
    except ValueError:
        return None
    # 判断Hosts规则类型
    if parts[0] in BLOCK_IP:
        value = parts[1]
        return "HOSTS", value
    return None


def parse_adblock_rules(line):
    # 删除不支持的规则
    value = line
    if value.startswith("@@"):
        return None
    if value.startswith(("http://","https://")):
        return None
    if "$" in value:
        modifiers = [
            modifier.split("=", 1)[0]
            for modifier in value.split("$", 1)[1].split(",")
        ]
        if any(
            modifier in modifiers
            for modifier in UNSUPPORTED_MODIFIER
        ):
            return None
    value = value.split("$", 1)[0]
    # 处理正则规则
    if value.startswith("/") and value.endswith("/"):
        value = value[1: -1]
        value = f"^{value}$"
        return "DOMAIN-REGEX", value
    # 处理域名规则
    if not value:
        return None
    value = value.lower()
    if "^" in value:
        value = value.split("^", 1)[0]
    if "/" in value:
        value = value.split("/", 1)[0]
    # 处理其他规则
    if value.startswith("||"):
        value = value[2:]
        if "*" in value:
            if  value.startswith("*."):
                if "*" in value[2:]:
                    return None
                return "DOMAIN-WILDCARD", value
            return None
        return "DOMAIN-SUFFIX", value
    if value.startswith("|"):
        if value.endswith("|"):
            value = value[1: -1]
            return "DOMAIN", value
        value = value[1:]
        return "DOMAIN", value
    if "*" in value:
        if  value.startswith("*."):
            if "*" in value[2:]:
                return None
            return "DOMAIN-WILDCARD", value
        return None
    return "DOMAIN", value


def parse_hosts_rules(line):
    value = line.lower()
    return "DOMAIN", value


def parse_domain_rules(line):
    value = line.lower()
    if value.startswith("+"):
        if value.startswith("+."):
            value = line[2:]
            return "DOMAIN-SUFFIX", value
        value = line[1:]
        return "DOMAIN-SUFFIX", value
    return "DOMAIN", value

def main():
    # 初始化
    OUTPUT_DIR.mkdir(
        exist_ok=True
    )
    # 检测规则类型
    for input_file in INPUT_DIR.glob("*.txt"):
        rules = set()
        print(
            f"Parsing: {input_file}"
        )
        with input_file.open(
            encoding="utf-8"
        ) as f:
            for line in f:
                result = detect_type(line)
                if not result:
                    continue
                rule_type, value = result
                # 根据类型处理规则
                if rule_type == "ADBLOCK":
                    value = parse_adblock_rules(value)
                elif rule_type == "HOSTS":
                    value = parse_hosts_rules(value)
                elif rule_type == "DOMAIN":
                    value = parse_domain_rules(value)
                if not value:
                    continue
                rules.add(value)
        # 输出信息
        print(
            f"Found {len(rules)} rules"
        )
        # 输出规则
        output_file = OUTPUT_DIR / (
            input_file.stem + ".yaml"
        )
        output_file.parent.mkdir(
            exist_ok=True
        )
        with output_file.open(
            "w",
            encoding="utf-8"
        ) as f:
            f.write("payload:\n")
            for kind, value in sorted(rules):
                f.write(
                    f"  - {kind},{value}\n"
                )


if __name__ == "__main__":
    main()