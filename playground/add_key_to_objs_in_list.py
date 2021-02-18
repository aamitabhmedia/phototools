l = [
    {"name": "Amitabh"},
    {"name": "Shailja"},
    {"name": "Ishika"}
]

print(l)

for o in l: o["shared"] = True

print(l)

# initialArr.forEach(v => {v["isActive"] = True})
# p = l.map(v => ({...v, 'shared': False}))
# p = map(lambda x: (x['shared'] = True; x), l)
# print(p)