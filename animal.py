class Animal:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def walk(self):
        return f"{self.name} is walking."

    def sleep(self):
        return f"{self.name} is sleeping."

    def bark(self):
        return f"{self.name} is barking."


class Dog(Animal):
    def __init__(self, name, color, breed):
        super().__init__(name, color)
        self.breed = breed

    def fetch(self):
        return f"{self.name} fetches the ball."

    def bark(self):
        return f"{self.name} the {self.breed} is barking: Woof!"


class Cat(Animal):
    def __init__(self, name, color, indoor=True):
        super().__init__(name, color)
        self.indoor = indoor

    def meow(self):
        return f"{self.name} is meowing: Meow!"

    def purr(self):
        return f"{self.name} is purring."

    def scratch(self):
        place = "the scratching post" if self.indoor else "a tree"
        return f"{self.name} scratches {place}."
