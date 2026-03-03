import re

pattern = r"^ab{2,3}$"

strings = ["abb", "abbb", "abbbb", "ab"]

for s in strings:
    if re.match(pattern, s):
        print(f"{s} -> Match")
    else:
        print(f"{s} -> No match")