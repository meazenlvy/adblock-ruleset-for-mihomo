from pathlib import Path
import subprocess
import yaml


# 配置
INPUT = Path("./process/merged/adblock.yaml")
OUTPUT = Path("./rules/adblock.mrs")
MIHOMO = Path("./bin/mihomo")
command = [
            str(MIHOMO),
            "convert-ruleset",
            "domain",
            "yaml",
            str(INPUT),
            str(OUTPUT),
        ]


# 创建目录
TEMP.parent.mkdir(
    exist_ok=True
)
OUTPUT.parent.mkdir(
    exist_ok=True
)

def build_mrs():
    # 初始化
    rules = set()
    # 输出信息
    print(
        f"Building: {INPUT}"
    )
    # 编译
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    # 报错输出信息
    if result.returncode != 0:
        print("Build failed:")
        print(result.stderr)
        return False
    # 输出信息
    print(
        f"Generated: {OUTPUT}"
    )

    return True


def main():
    # 编译
    build_mrs()


if __name__ == "__main__":
    main()