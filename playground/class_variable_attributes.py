class Metadata(object):
    def __init__(self, filename):
        self.filename = filename


m = Metadata("lake Merritt.jpg")
print(m.filename)

m.DateTaken = "2010:01:02 16:05:20"
print(m.DateTaken)

class Album(object):
    pass

a = Album()
a.name = "Album Name"
a.path = "Album Path"

print(f"{a.name}, {a.path}")
