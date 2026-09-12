from __future__ import annotations
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen, Request


# Define source rules
SOURCES = {
    "qy.txt": 
        "https://raw.githubusercontent.com/790953214/qy-Ads-Rule/main/black.txt",
    "SMAdHosts.txt":
        "https://raw.githubusercontent.com/2Gardon/SM-Ad-FuckU-hosts/refs/heads/master/SMAdHosts",
    "awavenue.mrs":
        "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.mrs",
    "DNS-Kuner.txt":
        "https://raw.githubusercontent.com/Kuner-mw/DNS-Kuner/main/FilterRules/blacklist.txt",
    "Hagezi-pro-plus.txt":
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/adblock/pro.plus.txt"
}
OUTPUT_DIR = Path("./sources")


def download_rules(url: str, path: Path, max_retries: int, timeout: int) -> bool:
    """ Download, retry when timing out. """
    # Download rules
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Downloading attempt: {attempt}/{max_retries}: {url}")
            request = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )
            with urlopen(request, timeout=timeout) as response:
                content = response.read()

            # Exclude empty rule
            if len(content) == 0:
                raise ValueError("Downloaded file is empty.")

            # Save rule
            path.write_bytes(content)
            print(f"Saved {path.name} ({len(content)}) bytes in {path}.")
            return True

        # Retry
        except (URLError, ValueError) as error:
            if attempt < max_retries:
                wait_time = min(2 ** attempt, 30)
                time.sleep(wait_time)
                print(f"Retrying in {wait_time} seconds…")

            # Fail
            else:
                print(f"Failed after {attempt} times: {error}")
                return False


def main() -> None:
    success = 0
    # Timer starts.
    start_time = time.time()

    # Download rules, retry when timing out
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    for filename, url in SOURCES.items():
        if filename.endswith((".txt", ".mrs")):
            if download_rules(
                    url,
                    OUTPUT_DIR / filename,
                    3,
                    10
                ):
                success += 1
        else:
            print(f"Unsupported type: {filename}")
            continue
    print(
        f"Finished: {success}/{len(SOURCES)}"
    )

    # Timer stops.
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()
