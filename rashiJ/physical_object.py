"""
Makes systems that are physical objects.

All physical objects are rectangular boxes that live on a rectangular
surface, called the habitat area.
The habitat area has a Cartesian coordinate system with the origin at the
bottom left corner.

^
y
|________________________
|                        |
|                        |
|    habitat area        |
|                        |
|         __             |
|        |  |            |
|        |  |
|      (x,y)|
|                        |
O------------------------|--x>

- O: origin of coordinate system

A physical object is a system that defines the following variables:

    + x        --   The x-coordinate
    + y        --   The y-coordinate
    + mass     --   The mass
    + length_x --   The length in x direction
    + length_y --   The ...
    + height   --
    + volume   --
    + area

Author:
    Rashi

Date:
    7/22/2022
"""


__all__ = ["make_physical_system"]


from cdcm import *
from typing import Union



def make_physical_system(name_or_system : Union[str,System],
                         x=0.0 : float,
                         y=0.0 : float,
                         m=1.0 : float,
                         rho=None : Union[NoneType, float],
                         length_x=1.0 : float,
                         length_y=1.0 : float,
                         height=1.0 : float,
                         mass_units="kg" : str,
                         length_units="m" : str,
                         **kwargs):
    """A factory of physical objects.

    Arguments:
    name    --   A name for the object
    x       --   The initial x-coordinate of the object (default = 0). In meters.

    The **kwargs can be any arguments that a System takes.
    """
    if isinstance(name_or_system, str):
        # I am making a new system
        sys = System(name=name_or_system, **kwargs)
    elif isinstance(name_or_system, System):
        # I am just adding variables to an existing system
        sys = name_or_system
    else:
        raise ValueError(f"I do not know what to do with {type(name_or_system)}!")

    with sys:
        x = Variable(name="x", value=x, units=length_units)
        y = Variable(name="y", value=y, units=length_units)
        length_x = Variable(name="length_x", value=length_x, units=length_units)
        length_y = Variable(name="length_y", value=length_y, units=length_units)
        height = Variable(name="height", value=height, units=length_units)
        area = Variable(name="area", value=0.0, units=length_units+"^2")
        @make_function(area)
        def calculate_area(lx=length_x, ly=length_y):
            return lx * ly
        volume = Variable(name="volume", value=0.0, units=length_units+"^3")
        @make_function(volume)
        def calculate_volume(A=area, h=height):
            return A * h
        density = Variable(name="density", value=0.0,
                           units=mass_units + "/" + volume.units)
        mass = Variable(name="mass", value=0.0, units=mass_units)
        if rho is not None:
            # User gave me the density. I am ignoring the mass.
            density.value = rho
            @make_function(mass)
            def calculate_mass(V=volume, r=density):
                return r * V
        else:
            # User did not gave me the density. I am using the mass.
            mass.value = m
            @make_function(density)
            def calculate_density(V=volume, m=mass):
                return m / V

    return sys


if __name__ == "__main__":
    # Make a clock and give it attributes of a physical system
    clock = make_clock(dt=0.5, units="hrs")
    make_physical_system(clock, rho=0.5)
    print(clock)

    solar = make_physical_system("solar", description="Solar panels.")
    with solar:
        energy = Variable(name="energy", value=0.0)

    print(solar)

    # solar2 = make_power_generator(
    #     make_flamable(
    #         make_physical_system("solar", description="Solar panels.")
    #     )
    # )
    # with solar:
    #     energy = Variable(name="energy", value=0.0)
