with open("sample.txt", "a") as f:
    f.write("New line added\n")

with open("sample.txt", "r") as f:
    print(f.read())