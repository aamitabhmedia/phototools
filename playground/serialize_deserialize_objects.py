import context; context.set_context()
import json
from types import SimpleNamespace

import util

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
print(f"type: {type(p)}, {p.name}, {p.dob}, {p.address.street}")
print(p.address)

# -------------------------------------

# images = None
# with open('C:\\Users\\amitabh\\.phototools\\cache\\google_images.json') as json_file:
#     images = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))

# -------------------------------------

class GoogleAlbumCache(object):
    def __init__(self) -> None:
        self.albums = []
        self.ids = {}
        self.titles = {}

album_cache = GoogleAlbumCache()

class GoogleAlbum(object):
    def __init__(self) -> None:
        self.id = None
        self.title = None


# -------------------------------------

i = {"name": "01 holi party", "aperture": "3.5"}
print(i)

data = json.dumps(i, sort_keys=True, indent=4, default=lambda o: o.__dict__)
print(data)
p = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
print(f"{p.name}, {p.aperture}")

# -------------------------------------

print("# ------------------------------------")
google_cache = {
    'album_ids': {
        "albumid01": {
            'title': "album id title 01",
            'image_count': 21
        },
        "albumid02": {
            'title': "album id title 02",
            'image_count': 22
        }
    },
    'summary': {
        'album_count': 50,
        'image_count': 49330
    }
}
data = json.dumps(google_cache, sort_keys=True, indent=4, default=lambda o: o.__dict__)
google_cache_avatar = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# util.pprint(google_cache_avatar.album_ids.albumid01)
util.pprint(google_cache_avatar)


