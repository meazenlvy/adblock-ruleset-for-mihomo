from __future__ import annotations
import ipaddress
import time
from pathlib import Path


INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./process/parsed")


def detect_type(line: str) -> tuple[str, str] | None:
    BLOCK_IP = {
        "0.0.0.0",
        "127.0.0.1",
        "::",
        "::1"
    }

    # Exclude empty rules and comments
    rule = line.strip()
    if (
        not rule
        or rule.startswith("#")
        or rule.startswith("!")):
        return None

    # Detect adblock rules and domain rules
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

    # Detect hosts rules
    if parts[0] in BLOCK_IP:
        rule = parts[1]
        return "HOSTS", rule

    # Other unsopported rules
    return None


def parse_adblock(line: str) -> str | None:
    UNSUPPORTED_MODIFIER= (
        "badfilter",
        "denyallow",
        "script",
        "image",
        "css",
        "third-party",
        "popup")
    rule = line

    # Exclude unsupported rules
    if rule.startswith("@@"):
        return None
    if "http://" in rule or "https://" in rule:
        return None

    # Parse rules with modifiers
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

    # Exclude regex rules
    if rule.startswith("/") and rule.endswith("/"):
        return None

    # Parse suffix rules and domain rules
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


def parse_hosts(line: str) -> str :
    rule = line.lower()
    return rule


def main() -> None:
    # Timer starts. 
    start_time = time.time()

    # Parse rules
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

                # Parse rules according to types
                if rule_type == "ADBLOCK":
                    rule = parse_adblock(rule)
                elif rule_type == "HOSTS":
                    rule = parse_hosts(rule)
                elif rule_type == "DOMAIN":
                    pass
                else:
                    continue

                # Exclude empty rules
                if rule is None or not rule:
                    continue
                if rule.startswith("+."):
                    if not rule[2:]:
                        continue
                rules.add(rule)

        # Save parsed rules
        print(
            f"Found {len(rules)} rules"
        )
        OUTPUT_DIR.mkdir(
            exist_ok=True
        )
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

    # Timer stops.
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()
