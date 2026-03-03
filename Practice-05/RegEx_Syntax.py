import re

txt = "The rain in Spain"
y = re.findall("\d", txt)
x = re.findall("[a-m]", txt)
z = re.findall("Sp..n", txt)
t = re.findall("^The", txt)
if t:
  print("Yes, the string starts with 'hello'")
else:
  print("No match")
u = re.findall("Spain$", txt)
if u:
  print("Yes, the string ends with 'planet'")
else:
  print("No match")
i = re.findall("Sp.*n", txt)
print(x)
print(y)
print(z)
print(t)
print(u)
