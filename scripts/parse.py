import ipaddress
from pathlib import Path


# Define variables.
INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./temp")

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


# Define detect function.
def detect_type(line):

# Delete comments and blanks.
    value = line.strip()
    if (
        not value
        or value.startswith("#")
        or value.startswith("!")):
        return None

# Detect adblock and domain.
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

# Detect hosts.
    if parts[0] in BLOCK_IP:
        value = parts[1]
        return "HOSTS", value
    return None

# Define parse function for adblock rules.
def parse_adblock_rules(line):

# Delete whitelists and unsupporte rules.
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

# Parse regex rules.
    if value.startswith("/") and value.endswith("/"):
        value = value[1: -1]
        return "DOMAIN-REGEX", value

# Parse domain rules.
    if not value:
        return None
    value = value.lower()
    if "^" in value:
        value = value.split("^", 1)[0]
    if "/" in value:
        value = value.split("/", 1)[0]

# Parse other rules.
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

# Define parse functions for hosts.
def parse_hosts_rules(line):

    value = line.lower()
    return "DOMAIN", value

# Define parse function for domain.
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

# Detect types.
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

# Parse accirding to types.
                if rule_type == "ADBLOCK":
                    value = parse_adblock_rules(value)
                elif rule_type == "HOSTS":
                    value = parse_hosts_rules(value)
                elif rule_type == "DOMAIN":
                    value = parse_domain_rules(value)
                if not value:
                    continue
                rules.add(value)
        print(
            f"Found {len(rules)} rules"
        )

# Write.
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