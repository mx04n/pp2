import re

def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(snake_to_camel("hello_world_example"))