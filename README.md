# RouterOS CN IP Rules

Daily generated RouterOS address-list import file for China IPv4 and IPv6 CIDRs.

- `CN.rsc`: ready-to-import commands for `/ip firewall address-list` (`CN`) and `/ipv6 firewall address-list` (`CN-IPv6`).
- `CN.count.txt`: current entry counts.
- `CN.source.txt`: upstream source URL.

The generator fetches the single mixed-family source [MetaCubeX/meta-rules-dat `cn.list`](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list), validates each CIDR, and separates IPv4 and IPv6 into their respective RouterOS address lists. It refuses to publish if either family is missing.

GitHub Actions refreshes the output daily at 02:17 UTC (10:17 China Standard Time), on changes to the generator, and on manual dispatch.

Import `CN.rsc` in RouterOS. IPv4 entries go to list `CN`; IPv6 entries go to list `CN-IPv6`.
