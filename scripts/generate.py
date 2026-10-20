#!/usr/bin/env python3
"""Fetch CN IPv4/IPv6 CIDRs and render RouterOS address-list import commands."""
from datetime import datetime, timezone
from ipaddress import ip_network
import subprocess

SOURCES = {
    "ipv4": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list",
    "ipv6": "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china6.txt",
}


def fetch(url: str, version: int) -> list[str]:
    result = subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error", "--max-time", "60", url],
        check=True, capture_output=True, text=True, encoding="utf-8-sig",
    )
    text = result.stdout
    networks: list[str] = []
    for line_number, raw in enumerate(text.splitlines(), 1):
        value = raw.split("#", 1)[0].strip()
        if not value:
            continue
        network = ip_network(value, strict=False)
        # Some upstreams may include both families; keep only the requested one.
        if network.version == version:
            networks.append(str(network))
    if not networks:
        raise ValueError(f"{url}: no IPv{version} networks received; refusing to publish empty output")
    return networks


def main() -> None:
    ipv4 = fetch(SOURCES["ipv4"], 4)
    ipv6 = fetch(SOURCES["ipv6"], 6)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Generated at: {generated}",
        f"# IPv4 source: {SOURCES['ipv4']}",
        f"# IPv6 source: {SOURCES['ipv6']}",
        f"# Count: IPv4={len(ipv4)}, IPv6={len(ipv6)}",
        "/ip firewall address-list",
    ]
    lines.extend(f'add list=CN address={ip} comment="CN MetaCubeX"' for ip in ipv4)
    lines.append("/ipv6 firewall address-list")
    lines.extend(f'add list=CN-IPv6 address={ip} comment="CN IPv6"' for ip in ipv6)
    with open("CN.rsc", "w", encoding="utf-8", newline="\n") as output:
        output.write("\n".join(lines) + "\n")
    with open("CN.count.txt", "w", encoding="ascii") as output:
        output.write(f"IPv4={len(ipv4)}\nIPv6={len(ipv6)}\nTotal={len(ipv4) + len(ipv6)}\n")
    with open("CN.source.txt", "w", encoding="utf-8") as output:
        output.write("IPv4: " + SOURCES["ipv4"] + "\nIPv6: " + SOURCES["ipv6"] + "\n")
    print(f"Generated CN.rsc: IPv4={len(ipv4)}, IPv6={len(ipv6)}")


if __name__ == "__main__":
    main()
