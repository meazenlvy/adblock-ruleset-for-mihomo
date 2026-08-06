import ipaddress
from pathlib import Path

INPUT = Path("../sources/adguard.txt")
OUTPUT = Path("../output/ruleset.yaml")

def parse_ip(value):
    try:
        network = ipaddress.ip_network(value, strict=False)
        if network.version == 4:
            return "IP-CIDR", str(network)
        else:
            return "IP-CIDR6", str(network)
    except ValueError:
        return None

def parser(line):
    value = line.strip()
    if not value:
        return None
    if value.startswith(("0.0.0.0", "127.0.0.1", "::1", "::")):
        parts = value.split()
        if len(parts) < 2:
            return None
        value = parts[1].lower()
        ip_value = parse_ip(value)
        if ip_value:
            return ip_value
        if "." not in value:
            return None
        return "DOMAIN", value

    if (
        value.startswith("!")
        or value.startswith("#")
        or value.startswith("@@")
        or not value.startswith("||")
    ):
        return None
    if "$" in value:
        if "$important" in value:
            value = value.split("$", 1)[0]
        else:
            return None
    value = value[2:]
    if "^" in value:
        value = value.split("^", 1)[0]
    ip_value = parse_ip(value)
    if ip_value:
        return ip_value
    if "/" in value:
        value = value.split("/", 1)[0]
    if "." not in value:
        return None
    value = value.lower()
    if "*" in value:
        return "DOMAIN-WILDCARD", value
    return "DOMAIN-SUFFIX", value

def main():
    rules = set()
    with INPUT.open(
        encoding="utf-8"
    ) as f:
        for line in f:
            result = parser(line)
            if not result:
                continue
            rules.add(result)
    print(
        f"Found {len(rules)} rules"
    )

    OUTPUT.parent.mkdir(
        exist_ok=True
    )
    with OUTPUT.open(
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