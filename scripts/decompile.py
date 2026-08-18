from pathlib import Path
import subprocess


INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./output")

MIHOMO = Path("./bin/mihomo")


def convert(mrs_file):

    yaml_file = OUTPUT_DIR / (
        mrs_file.stem + ".yaml"
    )

    subprocess.run(
        [
            str(MIHOMO),
            "convert-ruleset",
            "mrs",
            "yaml",
            str(mrs_file),
            str(yaml_file),
        ],
        check=True,
    )

    print(
        f"Converted: {mrs_file} -> {yaml_file}"
    )


def main():

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    for mrs in INPUT_DIR.glob("*.mrs"):
        convert(mrs)


if __name__ == "__main__":
    main()