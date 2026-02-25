import json

with open() as f:
    data = json.load(f)

print("Interface Status")
print("=" * 79)
print("{:<50} {:<20} {:<6} {:<6}".format("DN", "Description", "Speed", "MTU"))
print("-" * 50, "-" * 20, "-" * 6, "-" * 6)

for item in data.get("imdata", []):
    attrs = item.get("l1PhysIf", {}).get("attributes", {})
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    print("{:<50} {:<20} {:<6} {:<6}".format(dn, descr, speed, mtu))