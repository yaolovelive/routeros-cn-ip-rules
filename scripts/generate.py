#!/usr/bin/env python3
"""Convert the mixed-family MetaCubeX CN CIDR list into RouterOS commands."""
from datetime import datetime, timezone
from ipaddress import ip_network
import subprocess

SOURCE = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list"


def fetch_networks() -> tuple[list[str], list[str]]:
    result = subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error", "--max-time", "60", SOURCE],
        check=True, capture_output=True, text=True, encoding="utf-8-sig",
    )
    ipv4: list[str] = []
    ipv6: list[str] = []
    for line_number, raw in enumerate(result.stdout.splitlines(), 1):
        value = raw.split("#", 1)[0].strip()
        if not value:
            continue
        try:
            network = ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError(f"{SOURCE}:{line_number}: invalid CIDR {value!r}") from exc
        (ipv4 if network.version == 4 else ipv6).append(str(network))
    if not ipv4 or not ipv6:
        raise ValueError(
            f"{SOURCE}: expected both address families, got IPv4={len(ipv4)}, IPv6={len(ipv6)}; refusing to publish"
        )
    return ipv4, ipv6


def main() -> None:
    ipv4, ipv6 = fetch_networks()
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Generated at: {generated}",
        f"# Source: {SOURCE}",
        f"# Count: IPv4={len(ipv4)}, IPv6={len(ipv6)}",
        "/ip firewall address-list",
    ]
    lines.extend(f'add list=CN address={ip} comment="CN MetaCubeX"' for ip in ipv4)
    lines.append("/ipv6 firewall address-list")
    lines.extend(f'add list=CN-IPv6 address={ip} comment="CN MetaCubeX"' for ip in ipv6)
    with open("CN.rsc", "w", encoding="utf-8", newline="\n") as output:
        output.write("\n".join(lines) + "\n")
    with open("CN.count.txt", "w", encoding="ascii") as output:
        output.write(f"IPv4={len(ipv4)}\nIPv6={len(ipv6)}\nTotal={len(ipv4) + len(ipv6)}\n")
    with open("CN.source.txt", "w", encoding="utf-8") as output:
        output.write(SOURCE + "\n")
    print(f"Generated CN.rsc: IPv4={len(ipv4)}, IPv6={len(ipv6)}")


if __name__ == "__main__":
    main()
