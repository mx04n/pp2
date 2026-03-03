import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

products = re.findall(r"\d+\.\n(.+)", text)

print("Products:")
for product in products:
    print(product)