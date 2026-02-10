class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)  # вызывает конструктор родителя
        self.gpa = gpa

    def display(self):
        print(f"Student: {self.name}, GPA: {self.gpa}")

s = Student("Alice", 3.8)
s.display()  # Student: Alice, GPA: 3.8
