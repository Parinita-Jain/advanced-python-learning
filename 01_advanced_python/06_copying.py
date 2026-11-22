
import copy

# Original configuration
original_config = {
    "application": "AI Assistant",
    "database": {
        "host": "localhost",
        "port": 3306
    },
    "settings": {
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

# Shallow copy
shallow_config = copy.copy(original_config)

# Deep copy
deep_config = copy.deepcopy(original_config)


# Modify nested dictionaries
shallow_config["database"]["port"] = 5432
deep_config["settings"]["temperature"] = 0.9


print("Original Configuration:")
print(original_config)

print("\nShallow Copy:")
print(shallow_config)

print("\nDeep Copy:")
print(deep_config)

print("\nObject identity checks:")

print(original_config is shallow_config)

print(original_config is deep_config)

print(shallow_config is original_config)

print(original_config["database"] is shallow_config["database"])

print(original_config["database"] is deep_config["database"])

a = [[1, 2], [3, 4]]
b = a

b[0][0] = 100

print(a)

#Here, b = a creates no copy whatsoever. Both variables refer to exactly the same outer list.