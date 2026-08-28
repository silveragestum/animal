from animal import Cat, Dog


def main():
    rex = Dog("Rex", "brown", "Labrador")
    bella = Dog("Bella", "black", "German Shepherd")
    whiskers = Cat("Whiskers", "orange", indoor=True)
    luna = Cat("Luna", "gray", indoor=False)

    dogs = [rex, bella]
    cats = [whiskers, luna]

    for dog in dogs:
        print(dog.walk())
        print(dog.sleep())
        print(dog.bark())
        print(dog.fetch())
        print()

    for cat in cats:
        print(cat.walk())
        print(cat.sleep())
        print(cat.meow())
        print(cat.purr())
        print(cat.scratch())
        print()


if __name__ == "__main__":
    main()
