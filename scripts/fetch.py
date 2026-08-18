from pathlib import Path
from urllib.request import urlopen, Request


# Define variables.
# Source rules.
SOURCES = {
    "qy.txt": 
        "https://raw.githubusercontent.com/790953214/qy-Ads-Rule/main/black.txt",

    "FuLing.txt":
        "https://raw.githubusercontent.com/Kuroba-Sayuki/FuLing-AdRules/main/FuLingRules/FuLingBlockList.txt",

    "SMAdHosts.txt":
        "https://raw.githubusercontent.com/2Gardon/SM-Ad-FuckU-hosts/refs/heads/master/SMAdHosts",

    "awavenue.mrs":
        "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.mrs"
}

TXT_OUTPUT_DIR = Path("./sources")
MRS_OUTPUT_DIR = Path("./sources")
YAML_OUTPUT_DIR = Path("./temp")


# Define download function.
def download_rules(url, path):

    print(f"Downloading: {url}")

    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urlopen(request, timeout=10) as response:
        content = response.read()

    path.write_bytes(content)

    print(
        f"Saved: {path} ({len(content)} bytes)"
    )

def main():

    TXT_OUTPUT_DIR.mkdir(
        exist_ok=True
    )
    YAML_OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    success = 0

# Download rules.
    for filename, url in SOURCES.items():
        if filename.endswith(".txt"):
            OUTPUT_DIR = TXT_OUTPUT_DIR
        elif filename.endswith(".yaml"):
            OUTPUT_DIR = YAML_OUTPUT_DIR
        elif filename.endswith(".mrs"):
            OUTPUT_DIR = MRS_OUTPUT_DIR
        else:
            print(f"Unsupported type: {filename}")
            continue
        try:
            download_rules(
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