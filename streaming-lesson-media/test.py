import json

string = "Historia y conversaci\xf3n"
string = string.encode('hex')

print(string.decode('hex'))
