class Vehicle:
    def start(self):
        print("Vehicle is starting")

class Car(Vehicle):
    def start(self):  # переопределяем метод
        print("Car is starting")

v = Vehicle()
v.start()  # Vehicle is starting

c = Car()
c.start()  # Car is starting
