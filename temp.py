import json
import pprint

with open("temp.txt", "a+") as f:
    # f.write("0987")
    f.seek(0)
    print(f.read())
