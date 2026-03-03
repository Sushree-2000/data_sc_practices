# 1
# Fibonacci Function
def fibonacci(n: int) -> int:
    # pass
    """Return the nth Fibonacci number, for positive n"""
    if 0<= n <= 1:
        return n
    n0, n1 = 0, 1
    res = None
    for i in range(n-1):
        res = n0+n1
        n1 = res
        n0 = n1
    return res

# for j in range(15):
#     print(j, fibonacci(j))


# 2
# Color Printing codes
BLACK = '\u001b[30m'
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLO = '\u001b[33m'
BLUE = '\u001b[34m'
MAGENTA = '\u001b[35m'
CYAN = '\u001b[36m'
WHITE = '\u001b[37m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
UNDERLINE = '\u001b[4m'
REVERSE = '\u001b[7m'

# print("This will be magenta.", MAGENTA)
def color_print(text: str, effect: str) -> None:
    """Print text using the ANSI sequence to change colour.
    :param text: The text to print.
    :param effect: The effect we want, one of the constants defined above."""
    output_str = "{0}{1}{2}".format(effect, text, RESET)
    print(output_str)
    
# color_print("This will be magenta.", MAGENTA, BOLD)
# print("and this will be the same")



# 3
# *args
numbers = (0,1,2,3,4,5)
# print(numbers, sep=";") # (0;1;2;3;4;5)
# print(*numbers, sep=";") # 0;1;2;3;4;5
# print(0,1,2,3,4,5, sep=";")



# 4
# print("This will be magenta.", MAGENTA)
def color_print2(text: str, *effects: str) -> None:
    """Print text using the ANSI sequence to change colour.
    :param text: The text to print.
    :param effects: The effect we want, one of the constants defined above."""
    effect_string = "".join(effects)
    output_str = "{0}{1}{2}".format(effect_string, text, RESET)
    # print(output_str)
    
# color_print2("This will be magenta.", MAGENTA, BOLD)
# print("and this will be the same")



# 5
# different parameter types
def func(p1, p2, *args, k, **kwargs):
    print("positional-or-keyword: ...{}, {}".format(p1, p2))
    print("var-positional (*args): ...{}".format(args))
    print("keyword: ...{}".format(k))
    print("var-keyword: ...{}".format(kwargs))

# func(1, 2, 3, 4, 5, k=6, key1=7, key2=8)



# 6 - Dictionary
fruit = {"orange": "orange", "apple":"red", "lemon":"green", "grape": "purple", "lime":"Torquise"}
veggies = {"cabbage":"green", "potato":"brown", "tomato":"red"}
while True:
    fruit_keys = fruit.keys()
    fruit_values = fruit.values()
    fruit_items = fruit.items() # Return elements as a list of tuples of key,value
    fruit['banana'] = 'yellow'
    copied_fruits = fruit.copy()
    copied_fruits.update(veggies)
    # dict_key = input("Enter a fruit: ")
    # if dict_key == "quit":
    #     break
    # description = fruit.get(dict_key, "We don't have a "+dict_key)

    # print(list(fruit_items),list(fruit_keys), list(fruit_values), copied_fruits)
    break



# 7- Sets
# singletone elems = list: [1], tuple: (1,), dict: {'key':'value'}, set: {1}
# empty elems = list: [], tuple: (), dict: {}, set: set{}
farm_animals = {"sheep", "cow", "hen"}
wild_animals = {'lion', 'tiger', 'fox'}
farm_animals.add("horse") #to add new element 
sorted(farm_animals) #tosort the set
wild_animals.issubset(farm_animals) # to concat two sets
wild_animals.issuperset(farm_animals) # to concat two sets
wild_animals.union(farm_animals) # to concat two sets
wild_animals.intersection(farm_animals) # to get the common elements of the two sets
wild_animals.difference(farm_animals) # to get the elements of wild animals that are not in farm_animals
wild_animals.difference_update(farm_animals) # Removes all elements from wild_animals that are also in farm_animals.
wild_animals.symmetric_difference(farm_animals) # Return a new set with elements in either the set or other but not both.
frozenset((1,2,3,4)) # immutable



# 8 input/output
check = open("/Users/subha/Desktop/FlaskProject/txtFiles/Sample.txt")
for lines in check:
    if "The" in lines.lower():
        # print(lines, end='')
        pass    

check.close()

with open("/Users/subha/Desktop/FlaskProject/txtFiles/Sample.txt", 'r') as file:
    for line in file:
        if "The" in lines.lower():
            # print(lines, end='')
            pass 
            
with open("/Users/subha/Desktop/FlaskProject/txtFiles/Sample.txt", 'r') as file:
    line = file.readline()
    while line:
        # print(lines, end='')
        pass 
        line = file.readline()


with open("/Users/subha/Desktop/FlaskProject/txtFiles/binary.py", 'wb') as bin_file:
    for i in range(17):
        bin_file.write(bytes([i]))

with open("/Users/subha/Desktop/FlaskProject/txtFiles/binary.py", 'rb') as binFile:
    for b in binFile:
        # print(b)
        pass

import shelve

with shelve.open("bike.db") as bike:
    bike['make'] = 'Honda'
    bike['model'] = '250 dream'
    bike['colour'] = 'red'
    bike['engine_size'] = 250

    print(bike['colour'])
    print(bike['model'])

import dbm
print(dbm.whichdb("bike"))