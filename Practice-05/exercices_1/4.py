import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

if datetime_match:
    print("Date and time:", datetime_match.group())
else:
    print("Date and time not found")