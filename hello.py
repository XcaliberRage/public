from cs50 import get_string

while True:
    s = get_string("What is your name? ")
    if s != "":
        break

print("Hello, ", s)