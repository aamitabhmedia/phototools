import os
import json

val = {
    'title': None,
    'id': "sdof345kmfi3fm[48tig04mgsldfj"
}

data = json.dumps(val, indent=2)

filepath = os.path.join(os.getcwd(), "serialized_none.json")
with open(filepath, 'w') as writer:
    json.dump(val, writer, indent=2)

with open(filepath, 'r') as reader:
    val = json.load(reader)
    print(val)
    if val.get('title') is None:
        print("title is None")