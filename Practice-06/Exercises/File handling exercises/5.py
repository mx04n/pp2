import os

file_name = "backup_sample.txt"

if os.path.exists(file_name):
    os.remove(file_name)
    print("File deleted")
else:
    print("File not found")