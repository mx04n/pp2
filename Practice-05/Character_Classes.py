import re

txt = "The rain in Spain"


x = re.findall("[arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

y = re.findall("[a-n]", txt)

print(y)

if y:
  print("Yes, there is at least one match!")
else:
  print("No match")

z = re.findall("[0123]", txt)

print(z)

if z:
  print("Yes, there is at least one match!")
else:
  print("No match")
pp = "8 times before 11:45 AM"

t = re.findall("[+]", pp)

print(t)

if t:
  print("Yes, there is at least one match!")
else:
  print("No match")
