from pathlib import Path
import yaml


# Define variables.
INPUT_DIR = Path("./temp")
OUTPUT = Path("./rules/adblock.yaml")


# Define load function.
def load_rules(path):

    with path.open(
        encoding="utf-8"
    ) as f:
        data = yaml.safe_load(f) or {}

# yaml
    if isinstance(data, dict):
        return data.get(
            "payload",
            []
        )

# domain-only
    if isinstance(data, str):
        rules = []
        for line in data.splitlines():
            line = line.strip()

            if not line:
                continue
            if line.startswith("#"):
                continue

            # +xxx 转 DOMAIN-SUFFIX
            if line.startswith("+."):
                line = line[2:]
                rules.append(
                    f"DOMAIN-SUFFIX,{line}"
                )
            elif line.startswith("+"):
                line = line[1:]
                rules.append(
                    f"DOMAIN-SUFFIX,{line}"
                )
            else:
                rules.append(
                    f"DOMAIN,{line}"
                )

        return rules
    return []



def main():

    rules = set()

    for file in INPUT_DIR.glob("*.yaml"):
        print(
            f"Loading: {file}"
        )

        for rule in load_rules(file):
            rules.add(rule)
    print(
        f"Total rules: {len(rules)}"
    )

    OUTPUT.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:

        yaml.dump(
            {
                "payload": sorted(rules)
            },
            f,
            allow_unicode=True,
            sort_keys=False
        )


if __name__ == "__main__":
    main()