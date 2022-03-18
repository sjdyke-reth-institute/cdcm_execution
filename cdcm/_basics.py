"""Some very basic types to simplify the code that is coming later.

Author:
    Ilias Bilionis

Date:
    3/17/2022

"""


__all__ = ["NamedType"]


from abc import ABC


class NamedType(ABC):
    """A named type is a type that has a name.

    Keyword Arguments:
    name        -- The name of the object. The user must definitely provide a
                   name.
    description -- The description of the object. Optional.
    """

    def __init__(self, *, name="unamed_named_type", description=""):
        assert isinstance(name, str), \
            f"{name} is not a string. Names must be strings!"
        self._name = name
        assert isinstance(description, str), \
            f"{description} is not a string. Descriptions must be strings."
        self._description = description

    @property
    def name(self):
        """Get the name of the object."""
        return self._name

    @property
    def description(self):
        """Get the description of the object."""
        return self._description

    def __str__(self):
        """Return a string representation of the object."""
        return self.name

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        return {
            self.name: {"description": self.description,
                        "type": self.__class__.__name__}}

    def from_yaml(self, data):
        """Set the parameters of the object from a dictionary."""
        assert len(data) == 1, (f"{data} contains multiple items. It must only"
                                + " contain one item corresponding to a named"
                                + " object.")
        self._name = data.keys()[0]
        self._description = data.values()["description"]
