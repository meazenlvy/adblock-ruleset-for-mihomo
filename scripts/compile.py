from __future__ import annotations
import time
import subprocess
from pathlib import Path


INPUT = Path("./process/merged/adblock.txt")
OUTPUT = Path("./rules/adblock.mrs")
MIHOMO = Path("./bin/mihomo")


def build_mrs() -> bool:
    OUTPUT.parent.mkdir(
        exist_ok=True
    )
    command = [
        str(MIHOMO),
        "convert-ruleset",
        "domain",
        "text",
        str(INPUT),
        str(OUTPUT),
    ]

    # Compile rules
    print(
        f"Building: {INPUT}"
    )
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    # Capture error
    if result.returncode != 0:
        print("Build failed:")
        print(result.stderr)
        return False

    # Print success info
    print(
        f"Generated: {OUTPUT}"
    )

    return True


def main() -> None:
    # Timer starts.
    start_time = time.time()

    # Compile
    build_mrs()

    # Timer stops.
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()
