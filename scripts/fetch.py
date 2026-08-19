from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import time


# 配置
SOURCES = {
    "qy.txt": 
        "https://raw.githubusercontent.com/790953214/qy-Ads-Rule/main/black.txt",

    "SMAdHosts.txt":
        "https://raw.githubusercontent.com/2Gardon/SM-Ad-FuckU-hosts/refs/heads/master/SMAdHosts",

    "awavenue.mrs":
        "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.mrs"
}
OUTPUT_DIR = Path("./sources")


# 自动重试的下载
def download_rules(url, path, max_retries, timeout):
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

            if len(content) == 0:
                raise ValueError("Downloaded file is empty.")

            path.write_bytes(content)
            print(f"Saved {path.name} ({len(content)}) bytes in {path}.")
            return True
        except (URLError, ValueError) as e:
            if attempt < max_retries:
                wait_time = min(2 ** attempt, 30)
                print(f"Retrying in {wait_time} seconds…")
                time.sleep(wait_time)
            else:
                print(f"Failed after {attempt} times: {e}")
                return False


def main():
    # 初始化
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )
    success = 0
    start_time = time.time()
    # 下载规则
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
    # 输出
    print(
        f"Finished: {success}/{len(SOURCES)}"
    )
    # 计时
    last_time = time.time() - start_time
    print(f"Total time: {last_time:.2f} seconds.")


if __name__ == "__main__":
    main()