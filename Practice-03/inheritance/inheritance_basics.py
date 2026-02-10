# Родительский класс
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} издает звук")

# Наследник
class Dog(Animal):
    pass  # пока ничего не добавляем

dog = Dog("Рекс")
dog.speak()  # Рекс издает звук
