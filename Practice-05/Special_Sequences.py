import re

txt = "The rain in Spain"

x = re.findall("\AThe", txt)

print(x)

if x:
  print("Yes, there is a match!")
else:
  print("No match")
y = re.findall("\d", txt)

print(y)

if y:
  print("Yes, there is at least one match!")
else:
  print("No match")
z = re.findall("\w", txt)

print(z)

if z:
  print("Yes, there is at least one match!")
else:
  print("No match")
