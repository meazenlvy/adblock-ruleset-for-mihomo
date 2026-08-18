from pathlib import Path
from urllib.request import urlopen, Request

SOURCES = {
    "yq.txt": 
        "https://raw.githubusercontent.com/790953214/qy-Ads-Rule/main/black.txt",

    "fuling.txt":
        "https://raw.githubusercontent.com/Kuroba-Sayuki/FuLing-AdRules/main/FuLingRules/FuLingBlockList.txt",
}

OUTPUT_DIR = Path("./sources")


def download(url, path):
    print(f"Downloading: {url}")

    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urlopen(request, timeout=30) as response:
        content = response.read()

    path.write_bytes(content)

    print(
        f"Saved: {path} ({len(content)} bytes)"
    )


def main():
    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    success = 0

    for filename, url in SOURCES.items():
        try:
            download(
                url,
                OUTPUT_DIR / filename
            )
            success += 1

        except Exception as e:
            print(
                f"Failed: {filename}"
            )
            print(e)

    print(
        f"Finished: {success}/{len(SOURCES)}"
    )


if __name__ == "__main__":
    main()