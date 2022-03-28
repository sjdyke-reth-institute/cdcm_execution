"""A system that keeps track of time.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


__all__ = ["clock"]


from . import PhysicalStateVariable, make_system


@make_system
def clock(dt,
          *,
          t=PhysicalStateVariable(name="t",
                                  value=0.0,
                                  units="seconds",
                                  description="The simulation time.")
          ):
    """A simulation clock."""
    return t + dt
