import re

text = "aaa aa aaaaa aaaaaa bbb"

pattern1 = r'a{3}'
matches1 = re.findall(pattern1, text)
print("a{3}:", matches1) 

pattern2 = r'a{3,}'
matches2 = re.findall(pattern2, text)
print("a{3,}:", matches2)  

pattern3 = r'a{2,4}'
matches3 = re.findall(pattern3, text)
print("a{2,4}:", matches3)  