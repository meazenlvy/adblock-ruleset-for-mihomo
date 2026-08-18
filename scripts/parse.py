from pathlib import Path

INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./temp")

def parser(line):
    unsupported= ("badfilter","denyallow",)

    value = line.strip()
    if not value:
        return None
    if (
        value.startswith("!")
        or value.startswith("#")
        or value.startswith("@@")
    ):
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

    if "." not in value:
        return None
    value = value.lower()
    if "^" in value:
        value = value.split("^", 1)[0]
    if "/" in value:
        value = value.split("/", 1)[0]

    if value.startswith("||"):
        value = value[2:]
    elif value.startswith("|"):
        if value.endswith("|"):
            value = value[1: -1]
            return "DOMAIN", value
        value = value[1:]
        return "DOMAIN", value

    if  value.startswith("*"):
        return "DOMAIN-WILDCARD", value
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
                result = parser(line)

                if not result:
                    continue

                rules.add(result)
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