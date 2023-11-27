class MyClass:
    def __init__(self):
        pass

    def method1(self):
        pass

    def method2(self):
        pass

# Create an instance of the class
my_instance = MyClass()

# Get all function names defined in the class
function_names = [func for func in dir(my_instance) if callable(getattr(my_instance, func)) and not func.startswith("__")]

# Print the function names
print("Function names:", function_names)
