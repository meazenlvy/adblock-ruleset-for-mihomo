import ipaddress
from pathlib import Path

INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./temp")

BLOCK_IP = {
    "0.0.0.0",
    "127.0.0.1",
    "::",
    "::1"
  }

unsupported= (
    "badfilter",
    "denyallow",
    "script",
    "image",
    "css",
    "third-party",
    "popup")

def judge(line):
    value = line.strip()
    if (
        not value
        or value.startswith("#")
        or value.startswith("!")):
        return None
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
    if parts[0] in BLOCK_IP:
        value = parts[1]
        return "HOSTS", value
    return None

def parse_adblock(line):
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
            for modifier in unsupported
        ):
            return None
    value = value.split("$", 1)[0]

    if value.startswith("/") and value.endswith("/"):
        value = value[1: -1]
        return "DOMAIN-REGEX", value

    if not value:
        return None
    value = value.lower()
    if "^" in value:
        value = value.split("^", 1)[0]
    if "/" in value:
        value = value.split("/", 1)[0]

    if value.startswith("||"):
        value = value[2:]
        if  value.startswith("*."):
            return "DOMAIN-WILDCARD", value
        return "DOMAIN-SUFFIX", value
    if value.startswith("|"):
        if value.endswith("|"):
            value = value[1: -1]
            return "DOMAIN", value
        value = value[1:]
        return "DOMAIN", value
    if  value.startswith("*."):
        return "DOMAIN-WILDCARD", value
    return "DOMAIN", value

def parse_hosts(line):
    value = line.lower()
    return "DOMAIN", value

def parse_domain(line):
    value = line.lower()
    return "DOMAIN-SUFFIX", value

def main():
    for input_file in INPUT_DIR.glob("*.txt"):
        rules = set()
        print(
            f"Parsing: {input_file}"
        )
        with input_file.open(
            encoding="utf-8"
        ) as f:
            for line in f:
                result = judge(line)

                if not result:
                    continue

                rule_type, value = result
                if rule_type == "ADBLOCK":
                    value = parse_adblock(value)
                if rule_type == "HOSTS":
                    value = parse_hosts(value)
                if rule_type == "DOMAIN":
                    value = parse_domain(value)
                if not value:
                    continue
                rules.add(value)
        print(
            f"Found {len(rules)} rules"
        )
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