"""Testing the Node class.

Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


from cdcm import *
import yaml


n1 = Node(
    name="n1"
)
n2 = Node(
    name="n2"
)
n1.add_child(n2)

n3 = Node(
    name="n3"
)

n3.add_parent(n1)

n4 = Node(
    name="n4"
)

n3.add_parent(n4)


print(n1)
print(n2)
print(n3)
print(n4)


print("Before removing parent n1 from n3:")
print(n1)
print("After removing parent n1 from n3:")
n1.remove_child(n3)
print(n1)
print(n3)
n3.remove_parent(n4)
print(n3)
print(n4)

