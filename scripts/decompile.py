from pathlib import Path
import subprocess


# Define variables.
INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./sources")

MIHOMO = Path("./bin/mihomo")


# Define decompile function.
def decompile_mrs(mrs_file):

    yaml_file = OUTPUT_DIR / (
        mrs_file.stem + ".yaml"
    )

    subprocess.run(
        [
            str(MIHOMO),
            "convert-ruleset",
            "domain",
            "mrs",
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

# Decompile.
    for mrs_file in INPUT_DIR.glob("*.mrs"):
        decompile_mrs(mrs_file)


if __name__ == "__main__":
    main()