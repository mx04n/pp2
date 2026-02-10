class Flyer:
    def fly(self):
        print("Летает в небе")

class Swimmer:
    def swim(self):
        print("Плавает в воде")

class Duck(Flyer, Swimmer):
    pass

d = Duck()
d.fly()   # Летает в небе
d.swim()  # Плавает в воде
