import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

products = re.findall(r"\d+\.\n(.+)", text)
prices = re.findall(r"\d{1,3}(?:\s\d{3})*,\d{2}", text)
total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)
datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)
payment_match = re.search(r"Банковская карта", text)

data = {
    "products": products,
    "prices": prices,
    "total": total_match.group(1) if total_match else None,
    "datetime": datetime_match.group() if datetime_match else None,
    "payment_method": payment_match.group() if payment_match else None
}

print(json.dumps(data, indent=4, ensure_ascii=False))