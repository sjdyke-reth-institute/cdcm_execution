"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""


__all__ = ["SystemOfSystems"]



from collections.abc import Iterable


from . import System


class SystemOfSystems(System):
    """A class representing a system of systems.

    Keyword Arguments
    name        -- A name for the system.
    systems     -- A list of systems.
    description -- A description for the system.
    """

    def __init__(self, name="SystemOfSystems", sub_systems=[], description=None):
        # Sanity check
        assert isinstance(sub_systems, Iterable)
        for s in sub_systems:
            assert isinstance(s, System)
        self._sub_systems = sub_systems
        super().__init__(name=name, description=description)

    @property
    def sub_systems(self):
        return self._sub_systems

    def _gahter(self, attribute):
        """Gather an attribute from all subsystems.

        It is assuming that the attribute is a `dict`.
        """
        res = {}
        for s in self.sub_systems:
            res.update(getattr(s, attribute))
        return res

    @property
    def state(self):
        return self._gahter("state")

    @property
    def parameters(self):
        return self._gahter("parameters")

    @property
    def parents(self):
        return self._gahter("parents")

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
        for s in self.sub_systems:
            s._calculate_next_state(dt)

    def _transition(self):
        for s in self.sub_systems:
            s._transition()

    def __str__(self):
        """Return string representation of combined system."""
        res = super().__str__()
        res += f"\nSubsystems:     {list([s.name for s in self.sub_systems])}"
        return res
    