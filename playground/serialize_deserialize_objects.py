import json
from types import SimpleNamespace

class Address(object):
    def __init__(self, street, city) -> None:
        self.street = street
        self.city = city
    
class Person(object):

    def __init__(self, name, dob, address) -> None:
        self.name = name
        self.dob = dob
        self.address = address

p = Person("Amitabh", "1923-10-15", Address("Crystal", "Pleasanton"))

data = json.dumps(p, sort_keys=True, indent=4, default=lambda o: o.__dict__)
print(data)

p = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(f"{p.name}, {p.dob}, {p.address.street}")
print(p.address)

# -------------------------------------

i = {"name": "01 holi party", "aperture": "3.5"}
print(i)

data = json.dumps(i, sort_keys=True, indent=4, default=lambda o: o.__dict__)
print(data)
p = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(f"{p.name}, {p.aperture}")
