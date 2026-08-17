from pathlib import Path
import subprocess


INPUT = Path("../rules/adguard-dns.yaml")
OUTPUT = Path("../rules/adguard-dns.mrs")

MIHOMO = Path("./bin/mihomo")


def build_mrs():
    print(
        f"Building: {INPUT}"
    )

    command = [
        str(MIHOMO),
        "convert-ruleset",
        "classical",
        str(INPUT),
        str(OUTPUT),
    ]

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