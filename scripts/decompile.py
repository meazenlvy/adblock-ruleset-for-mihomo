from pathlib import Path
import subprocess


# Define variables.
INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./process/decompiled")

MIHOMO = Path("./bin/mihomo")


# Define decompile function.
def decompile_mrs(mrs_file):

    txt_file = OUTPUT_DIR / (
        mrs_file.stem + ".txt"
    )

    subprocess.run(
        [
            str(MIHOMO),
            "convert-ruleset",
            "domain",
            "mrs",
            str(mrs_file),
            str(txt_file),
        ],
        check=True,
    )

    print(
        f"Converted: {mrs_file} -> {txt_file}"
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