import json
from types import SimpleNamespace


# Define JSON data
JSONData = '{"Java": "3 Credits", "PHP": "2 Credits", "C++": "3 Credits", "hometown": {"name": "New York", "id": 123}}'

# Declare class to store JSON data into a python dictionary
class read_data(object):
  def __init__(self, jdata):
    self.__dict__ = json.loads(jdata)

# Assign object of the class
p = read_data(JSONData)

# Print the value of specific property
print(p.PHP)


class Hometown(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
class read_json(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

p = read_json(data)
print(p.name)
print(p.hometown)
print(p.hometown.name)

print(f"{p.name}, {p.hometown}, {p.hometown.name}")

p = Person("John Smith", Hometown("New York", 123))

jp = json.dumps(p, indent=4, default=lambda o: o.__dict__)
print (jp)

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
print(data)

p = json.loads(jp)
print(f"{p.name}, {p.hometown}, {p.hometown.name}")

# person_dict = json.loads(jp)
# p = Person(**person_dict)

p = GoodPerson(data)
print(f"{p.name}, {p.hometown}, {p.hometown.name}")

# Parse JSON into an object with attributes corresponding to dict keys.
# x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# print(x.name, x.hometown.name, x.hometown.id, x.unknwn)