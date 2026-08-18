from pathlib import Path
import yaml


INPUT_DIR = Path("./temp")
OUTPUT = Path("./rules/adguard-dns.yaml")


def load_rules(path):
    with path.open(
        encoding="utf-8"
    ) as f:
        data = yaml.safe_load(f)or {}

    return data.get(
        "payload",
        []
    )


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