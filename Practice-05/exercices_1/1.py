import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Цены вида 308,00 или 1 200,00
prices = re.findall(r"\d{1,3}(?:\s\d{3})*,\d{2}", text)

print("All prices:")
for p in prices:
    print(p)