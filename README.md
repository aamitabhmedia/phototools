# phototools
Tools to manipulate images, managing google photos, etc.

## gphoto
This packages has all the tools to work with local albums and google photos library

## Usage
```python
# Import google photos library and initialize the service
import gphoto
gphoto.init()

# Running modules under gphoto
from gphoto import folder_cache
cache = folder_cache.load("d:\\picsHres\\2040")
```
