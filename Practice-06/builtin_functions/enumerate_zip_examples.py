
words = ["apple", "banana", "cherry"]
for i, word in enumerate(words):
    print(f"{i}: {word}")

names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

for name, score in zip(names, scores):
    print(f"{name} -> {score}")

student_dict = dict(zip(names, scores))
print("Dictionary:", student_dict)