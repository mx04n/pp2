import re

text = "Hello, world. Python is great"

result = re.sub(r"[ ,\.]", ":", text)

print(result)