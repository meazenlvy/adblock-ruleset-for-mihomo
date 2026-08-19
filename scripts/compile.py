from pathlib import Path
import subprocess
import yaml


INPUT = Path("./process/merged/adblock.yaml")
OUTPUT = Path("./rules/adblock.mrs")
TEMP = Path("./process/temp/adblock.yaml")

MIHOMO = Path("./bin/mihomo")


def build_mrs():
    print(
        f"Building: {INPUT}"
    )

    command = [
                    str(MIHOMO),
                    "convert-ruleset",
                    "domain",
                    "yaml",
                    str(TEMP),
                    str(OUTPUT),
                ]

    rules = set()
    with INPUT.open(
        encoding="utf-8"
    ) as f:
        data = yaml.safe_load(f) or {}
    for line in data.get("payload", []):
        if "," not in line:
            continue
        rule_type, value = line.split(",", 1)
        value = value.strip()
        if rule_type == "DOMAIN":
            rules.add(value)
        elif rule_type == "DOMAIN-SUFFIX":
            rules.add(
                "+." + value
            )
        elif rule_type == "DOMAIN-WILDCARD":
            rules.add(
                "+" + value[1:]
            )
        else:
            continue

    TEMP.parent.mkdir(
        exist_ok=True
    )

    with TEMP.open(
        "w",
        encoding="utf-8"
    ) as f:
        f.write("payload:\n")
        for rule in sorted(rules):
            f.write(f"  - {rule}\n")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Build failed:")
        print(result.stderr)
        return False

    print(
        f"Generated: {OUTPUT}"
    )

    return True


def main():
    if not INPUT.exists():
        print(
            f"Missing input: {INPUT}"
        )
        return

    OUTPUT.parent.mkdir(
        exist_ok=True
    )

    build_mrs()


if __name__ == "__main__":
    main()