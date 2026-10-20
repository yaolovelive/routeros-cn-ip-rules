# RouterOS CN IP Rules

Daily generated RouterOS address-list import file for China IPv4 and IPv6 CIDRs.

- `CN.rsc`: ready-to-import commands for `/ip firewall address-list` (`CN`) and `/ipv6 firewall address-list` (`CN-IPv6`).
- `CN.count.txt`: current entry counts.
- `CN.source.txt`: upstream source URLs.

Sources:

- IPv4: [MetaCubeX/meta-rules-dat](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list)
- IPv6: [gaoyifan/china-operator-ip](https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china6.txt)

GitHub Actions refreshes the output daily at 02:17 UTC (10:17 China Standard Time), on changes to the generator, and on manual dispatch. The generator validates every CIDR, selects the expected address family from each source, and refuses to overwrite the published output if a source yields no usable networks.

Import `CN.rsc` in RouterOS. It creates IPv4 entries in list `CN` and IPv6 entries in list `CN-IPv6`.
