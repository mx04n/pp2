import re

txt = "Åland"

print(re.findall("\w", txt, re.ASCII))

print(re.findall("\w", txt))

print(re.findall("\w", txt, re.A))

x = "The rain in Spain"

print(re.findall("spain", x , re.DEBUG))

xtx = """Hi
my
name
is
Sally"""

print(re.findall("me.is", xtx, re.DOTALL))

print(re.findall("me.is", xtx))

print(re.findall("me.is", xtx, re.S))

t = "The rain in Spain"

print(re.findall("spain", t, re.IGNORECASE))

print(re.findall("spain", t, re.I))

ttt = """There
aint much
rain in 
Spain"""

print(re.findall("^ain", ttt, re.MULTILINE))

print(re.findall("^ain", ttt))

print(re.findall("^ain", ttt, re.M))

print(re.findall("\w", txt, re.UNICODE))

print(re.findall("\w", txt, re.U))

text = "The rain in Spain falls mainly on the plain"

pattern = """
[A-Za-z]* #starts with any letter
ain+      #contains 'ain'
[a-z]*    #followed by any small letter
"""
print(re.findall(pattern, text, re.VERBOSE))

print(re.findall(pattern, text))

print(re.findall(pattern, text, re.X))

