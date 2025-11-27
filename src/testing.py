from enum import Enum
hi = {}

class enum(Enum):
    Two = 1
    Three = 2
    Four = 3

for enum_val in enum:
    hi[enum_val.name] = f"assets/{enum_val.name}" 


print("hi")
#EnumPaths : hi[Enum, str] = {}