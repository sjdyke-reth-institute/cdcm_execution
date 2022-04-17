"""A system that keeps track of time.

Author:
    Ilias Bilionis

Date:
    3/15/2022
    4/16/2022

"""


__all__ = ["make_clock"]


from . import make_node, make_function, System


def make_clock(
    dt,
    t0=0.0,
    dt_name="dt",
    t_name="t",
    units="seconds",
    description="A system that counts time.",
    clock_name="clock"
):
    """Make a clock system."""
    pdt = make_node(f"P:{dt_name}:{dt}:{units}", description="The timestep.")
    t = make_node(f"S:{t_name}:{t0}:{units}", description="The time.")
    @make_function(t)
    def tick(t=t, dt=pdt):
        """Moves time forward by `dt`."""
        return t + dt
    return System(
        name=clock_name,
        nodes=[pdt, t, tick],
        description=description
    )
