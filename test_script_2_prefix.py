# Error 1: Syntax Error
print("Welcome to the Error Program")
print("This program contains multiple errors.")

# Error 2: NameError
print("The value of x is: ", x)

# Error 3: TypeError
y = "5"
z = 10
result = y + z

# Error 4: IndexError
numbers = [1, 2, 3]
print(numbers[3])

# Error 5: ZeroDivisionError
a = 10
b = 0
result = a / b

# Error 6: IndentationError
print("This line has incorrect indentation.")
print("This line has correct indentation.")

# Error 7: AttributeError
message = "Hello, world!"
print(message.length)

# Error 8: ValueError
number = int("abc")

# Error 9: FileNotFoundError
file = open("nonexistent_file.txt", "r")

# Error 10: AssertionError
assert 2 + 2 == 5, "Math is broken!"

# Error 11: KeyError
dictionary = {"key": "value"}
print(dictionary["nonexistent_key"])
