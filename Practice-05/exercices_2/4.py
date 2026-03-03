import re

text = "Hello World TEST Python JavaScript"

pattern = r"\b[A-Z][a-z]+\b"

matches = re.findall(pattern, text)
print(matches)