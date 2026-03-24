import os

os.makedirs("example_dir/subdir", exist_ok=True)

for i in range(3):
    os.makedirs(f"example_dir/folder_{i}", exist_ok=True)

print("Содержимое example_dir:")
for item in os.listdir("example_dir"):
    print(item)