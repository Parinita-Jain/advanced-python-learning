"""
Objective: Understand how Python creates objects, tracks references, and removes objects that are no longer needed.
"""

import sys
import gc


# 1. Object identity and references

a = [10, 20, 30]
b = a

print("Object ID of a:", id(a))
print("Object ID of b:", id(b))
print("Same object:", a is b)


# 2. Reference count

x = [1, 2, 3]

print("\nReference count:", sys.getrefcount(x))

y = x

print("After creating y:", sys.getrefcount(x))

z = x

print("After creating z:", sys.getrefcount(x))


# 3. Deleting references

del y

print("\nAfter deleting y:", sys.getrefcount(x))


# 4. Garbage collection

print("\nGarbage collection:")
print("Unreachable objects collected:", gc.collect())

print("--------")

# Circular reference example
class Node:
    pass


node1 = Node()
node2 = Node()

node1.other = node2
node2.other = node1

del node1
del node2

print("Collected:", gc.collect())