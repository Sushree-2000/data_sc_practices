class Kettle(object):
    power_source = "electricity"
    def __init__(self, make, price):
        self.make = make
        self.price = price
        self.on = False

    def __str__(self):
        return "This is a {} kettle that costs {}.".format(self.make, self.price)
    
    def switch_on(self):
        self.on = True
    
kenwood = Kettle("Kenwood", 8.99)
print(kenwood.make, kenwood.price)

kenwood.price = 12.75
print(kenwood.make, kenwood.price)

hamilton = Kettle("Hamilton", 14.55)
print("Models: {}={}, {}={}".format(kenwood.make, kenwood.price, hamilton.make, hamilton.price))

"""
Class is a blueprint for creating objects. It defines a set of attributes and methods that the created objects will have. An object is an instance of a class, which means it is a specific realization of the class with its own unique data and behavior.
"""

print(hamilton.on)
hamilton.switch_on()
print(hamilton.on)

kenwood.switch_on()
print(kenwood.on)

print(Kettle.power_source)
print(hamilton.power_source)
print(kenwood.power_source)
print(kenwood.__dict__)