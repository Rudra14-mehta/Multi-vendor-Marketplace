from django.test import TestCase
import hashlib
# Create your tests here.
string = "Dhairya"

string = string.encode()
print(string)
string = hashlib.sha256(string).hexdigest()
# if lst:
#     print("non empty")
# else:
print(string)
