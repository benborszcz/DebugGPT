# test_script_2.py

# Error 1: Syntax Error
print("Welcome to the Error Program")
print("This program contains multiple errors.")

# Error 2: NameError
x = 0
print("The value of x is: ", x)

# Error 3: TypeError
y = "5"
z = 10
result = y + str(z)

# Error 4: IndexError
numbers = [1, 2, 3, 4]
print(numbers[3])

# Error 5: ZeroDivisionError
a = 10
b = 1
result = a / b

# Error 6: IndentationError
print("This line has incorrect indentation.")
print("This line has correct indentation.")

# Error 7: AttributeError
message = "Hello, world!"
print(len(message))

# Error 8: ValueError
number = 123

# Error 9: FileNotFoundError
file = open("existing_file.txt", "w")

# Error 10: AssertionError
assert 2 + 2 == 4, "Math is broken!"

# Error 11: KeyError
dictionary = {"key": "value"}
print(dictionary["key"])  # Access a valid key instead of 'nonexistent_key'
