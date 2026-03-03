import re

pattern = r"^ab*$"

strings = ["a", "ab", "abb", "abbb", "ac"]

for s in strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")