import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)

if total_match:
    total = total_match.group(1)
    print("Total from receipt:", total)
else:
    print("Total not found")