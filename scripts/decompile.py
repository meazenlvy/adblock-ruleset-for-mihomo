from pathlib import Path
import subprocess


# 配置
INPUT_DIR = Path("./sources")
OUTPUT_DIR = Path("./process/parsed")
MIHOMO = Path("./bin/mihomo")


# 创建文件夹
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def decompile_mrs(mrs_file):
    # 初始化
    txt_file = OUTPUT_DIR / (
        mrs_file.stem + ".txt"
    )
    # 调用命令反编译
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
    # 输出信息
    print(
        f"Converted: {mrs_file} -> {txt_file}"
    )


def main():
    # 反编译
    for mrs_file in INPUT_DIR.glob("*.mrs"):
        decompile_mrs(mrs_file)


if __name__ == "__main__":
    main()