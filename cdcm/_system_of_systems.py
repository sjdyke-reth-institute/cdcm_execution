"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


__all__ = ["SystemOfSystems"]


from . import System, _assert_and_make_dict, _dict_to_yaml, NamedType


class SystemOfSystems(System):
    """A class representing a system of systems.

    Keyword Arguments
    name        -- A name for the system.
    systems     -- A dictionary of systems. The keys must be strings. The
                   values must be `System`. Alternatively, a list of systems.
    description -- A description for the system.
    """

    def __init__(self,
                 name="system_of_systems",
                 sub_systems={},
                 description=""):
        # Sanity check
        sub_systems = _assert_and_make_dict(sub_systems, System)
        self._sub_systems = sub_systems
        super().__init__(name=name, description=description)

    @property
    def sub_systems(self):
        return self._sub_systems

    def _gather(self, attribute):
        """Gather an attribute from all subsystems.

        It is assuming that the attribute is a `dict`.
        """
        res = {}
        for s in self.sub_systems.values():
            res.update(getattr(s, attribute))
        return res

    @property
    def state(self):
        return self._gather("state")

    @property
    def parameters(self):
        return self._gather("parameters")

    @property
    def parents(self):
        return self._gather("parents")

    @property
    def fundamental_subsystems(self):
        """Get the fundamental subsystems.

        The fundamental subsystems are `Systems` that are not decomposable
        into simpler systems.
        """
        res = []
        for s in self.sub_systems:
            if not isinstance(s, SystemOfSystems):
                res.append(s)
            elif isinstance(s, System):
                res += s.fundamental_subsystems
            else:
                raise RuntimeError(f"{s} is not a System.")
        return res

    @property
    def can_transition(self):
        """Check if the system can transition.

        TODO: THIS IS NOT CORRECT>
        """
        raise NotImplementedError("Haven't implemented can_transition yet.")

    def _calculate_next_state(self, dt):
        for s in self.sub_systems.values():
            s._calculate_next_state(dt)

    def _transition(self):
        for s in self.sub_systems.values():
            s._transition()

    def __str__(self):
        """Return string representation of combined system."""
        res = super().__str__()
        res += f"\nSubsystems:     {list([n for n in self.sub_systems])}"
        return res

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        res = NamedType.to_yaml(self)
        dres = res[self.name]
        dres["sub_systems"] = _dict_to_yaml(self.sub_systems)
        return res
