from __future__ import annotations
import subprocess
import time
from pathlib import Path


INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./process/parsed")
MIHOMO = Path("./bin/mihomo")


def decompile(mrs_file: Path) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    txt_file = OUTPUT_DIR / (
        mrs_file.stem + ".txt"
    )

    # Decompile
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


def main() -> None:
    # Timer starts.
    start_time = time.time()

    # Decompile mrs files
    for mrs_file in INPUT_DIR.glob("*.mrs"):
        decompile(mrs_file)

    # Timer stops.
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()