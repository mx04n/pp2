import re

pattern = r"^a.*b$"

strings = ["ab", "acb", "a123b", "aXb", "ac"]

for s in strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")