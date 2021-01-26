from datetime import datetime

print("----- common")

_current_time = datetime.now()
print(f"current time: '{_current_time}'")

def curt():
    return _current_time