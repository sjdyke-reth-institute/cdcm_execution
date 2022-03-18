"""Test the basic types.

Author:
    Ilias Bilionis

Date:
    3/17/2022

"""


from cdcm import *
import yaml


if __name__ == "__main__":
    x = NamedType(name="foo", description="bar")
    print(x.to_yaml())
    print(yaml.dump(x.to_yaml(), sort_keys=False))

    q = Parameter(value=[0.5, 0.3],
                  name="q",
                  units="meters",
                  description="some desc")
    print(yaml.dump(q.to_yaml(), sort_keys=False))
