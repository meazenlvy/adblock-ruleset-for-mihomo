from pathlib import Path

INPUT = Path("../sources/adguard.txt")
OUTPUT = Path("../output/ads.yaml")

def parse_adguard_rule(line):
    line = line.strip()
    if not line or line.startswith("!"):
        return None
    if line.startswith("@@"):
        return None
    if not line.startswith("||"):
        return None
    domain = line[2:]
    domain = domain.split("^")[0]
    domain = domain.split("/")[0]
    if "." not in domain:
        return None
    if "*" in domain:
        return None
    return domain.lower()

def main():
    domains = set()
    with INPUT.open(
        encoding="utf-8"
    ) as f:
        for line in f:
            domain = parse_adguard_rule(line)
            if domain:
                domains.add(domain)
    print(
        f"Found {len(domains)} domains"
    )
    OUTPUT.parent.mkdir(
        exist_ok=True
    )
    with OUTPUT.open(
        "w",
        encoding="utf-8"
    ) as f:
        f.write("payload:\n")
        for domain in sorted(domains):
            f.write(
                f"  - DOMAIN-SUFFIX,{domain}\n"
            )

if __name__ == "__main__":
    main()