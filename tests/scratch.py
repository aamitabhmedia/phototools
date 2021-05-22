import os
import util
import pathlib

l = [1, 2, 3, 4, 5, 6, 7]
ll = len(l)

chunk_size = 5
i = 0
while i < ll:
    lc = l[i:(i+chunk_size)]
    print(lc)