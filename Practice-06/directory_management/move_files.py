import os
import shutil

with open("test.txt", "w") as f:
    f.write("Hello")

os.makedirs("dest", exist_ok=True)

shutil.move("test.txt", "dest/test.txt")

print("Файл перемещен!")