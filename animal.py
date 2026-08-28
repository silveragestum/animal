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
