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

    + name     --   ID of the object.
    + x        --   The x-coordinate
    + y        --   The y-coordinate
    + length_x --   The length in x direction
    + length_y --   The length in y direction
    + length_z --   The length in z direction
    + area     --   The surface area occupied by the object
    + volume   --   The volume occupied by the object
    + mass     --   The mass of the object
    + density  --   The density of the object.

Author:
    Rashi

Date:
    Orginal File - 7/22/2022
      The orginal file consisted of definitions for x, y, mass, length_x,
      length_y, height, are, volume, mass density.

      It included some conversions from mass to density, or vice versa.

    Edited Version 1 - 8/9/2022
      New Definition: ID
      Changed Definitions: height -> length_z

      More conversion: area -> length_x, length_y
                       length_x, length_y -> area
                       length_x, length_y, length_z -> volume
                       density, volume -> mass
                       mass, density -> volume

     Current: Code Syntax Error
              Check if new conversions have the correct structure.
"""

# All this code combines to make_physical_system
__all__ = ["make_physical_system"]


from cdcm import *
from typing import Union
from common import maybe_make_system

NoneType = type(None)


def make_physical_system(
    name_or_system: Union[str, System],
    x: float = 0.0,
    y: float = 0.0,
    length_x: float = 1.0,
    length_y: float = 1.0,
    length_z: float = 1.0,
    A: Union[NoneType, float] = None,
    m: float = 1.0,
    rho: Union[NoneType, float] = None,
    mass_units: str = "kg",
    length_units: str = "m",
    **kwargs
):

    """A factory of physical objects.

    Arguments:
    name    --   A name for the object
    x       --   The initial x-coordinate of the object (default = 0). In meters.

    The **kwargs can be any arguments that a System takes.
    """

    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:
        x = Variable(name="x", value=x, units=length_units)
        y = Variable(name="y", value=y, units=length_units)

        area = Variable(name="area", value=0.0, units=length_units + "^2")

        length_x = Variable(name="length_x", value=length_x, units=length_units)
        length_y = Variable(name="length_y", value=length_y, units=length_units)
        length_z = Variable(name="length_z", value=length_z, units=length_units)

        if area is not None:
            # User gave me the area. I am ignoring length_x, length_y
            area.value = A

            @make_function(length_x)
            def length_from_area(A=area):
                return A**0.5

            length_y = length_x
        else:
            # User did not give me the area. I am using length_x, length_y
            @make_function(area)
            def calculated_area(lx=length_x, ly=length_y):
                return lx * ly

        volume = Variable(name="volume", value=0.0, units=length_units + "^3")

        @make_function(volume)
        def calculate_volume(A=area, h=length_z):
            return A * h

        density = Variable(
            name="density", value=0.0, units=mass_units + "/" + volume.units
        )

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
