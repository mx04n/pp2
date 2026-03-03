import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

payment_match = re.search(r"Банковская карта", text)

if payment_match:
    print("Payment method:", payment_match.group())
else:
    print("Payment method not found")