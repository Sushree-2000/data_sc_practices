import os

def list_directories(s):

    def dir_list(d):
        nonlocal tab_stop
        files = os.listdir(d)
        for f in files:
            current_dir = os.path.join(d, f)
            if os.path.isdir(current_dir):
                print("\t" * tab_stop + f)
                tab_stop += 1
                dir_list(current_dir)
                tab_stop -= 1
            else:
                print("\t" * tab_stop + f)
    tab_stop = 0
    if os.path.exists(s):
        print("Directory exists" + s)
        dir_list(s)
    else:
        print("Directory does not exist" + s)
# listing = os.walk('.')
# for root, directories, files in listing:
#     print(root)
#     # print(directories)
#     # print(files)
#     for d in directories:
#         # print(os.path.join(root, d))
#         print(d)
#     for file in files:
#         print(file)

list_directories('.')




# nonlocal keyword is used to refer to a variable in the nearest enclosing scope that is not global. It allows you to modify a variable defined in an outer function from within an inner function. In the example above, the dir_list function is defined inside the list_directories function, and it uses the nonlocal keyword to access and modify the tab_stop variable defined in the list_directories function. This allows the dir_list function to keep track of the current level of indentation when printing the directory structure.

# NONLOCAL KEYWORD, FREE AND LEGB RULES