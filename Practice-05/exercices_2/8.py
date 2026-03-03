import re

text = "HelloWorldPython"

result = re.findall(r"[A-Z][^A-Z]*", text)

print(result)