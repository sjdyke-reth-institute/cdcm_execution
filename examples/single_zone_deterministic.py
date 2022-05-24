"""
Example of a single zone fully deterministic building made using YABML.

Author(s):
    Sreehari Manikkan
Date:
    05/11/2022
"""

from yabml import *

a = DeterministicParameter('m', 30)
b = DeterministicParameter('m', 15)
"""
Walls
-----
Walls are made of Brick wall type 19 given in ASHRAE handbook Table 16.
Wall area ratio is 0.75 and window area ratio is 0.25. The wall is
modeled as a segment consisting of 8 layers. The values of
parameters of layers provided are in British Pound system, but the units
are SI system as this example is for demonstration purpose.
"""
F01 = Layer(
    thickness=DeterministicParameter('inch', 0.001),
    conductivity=DeterministicParameter('W/m/degC', 0.001),
    density=DeterministicParameter('kg/m**3', 0.001),
    specific_heat=DeterministicParameter('J / kg / degC', 0.001),
    solar_transmittance=DeterministicParameter(None, 0.0),
    description='Outside surface resistance'
)
M01 = Layer(
    thickness=DeterministicParameter('inch', 4.0),
    conductivity=DeterministicParameter('W/m/degC', 6.2),
    density=DeterministicParameter('kg/m**3', 120.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.19),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='4 in. brick'
)
F04 = Layer(
    thickness=DeterministicParameter('inch', 0.001),
    conductivity=DeterministicParameter('W/m/degC', 0.001),
    density=DeterministicParameter('kg/m**3', 0.001),
    specific_heat=DeterministicParameter('J / kg / degC', 0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='Wall air space resistance'
)
I01 = Layer(
    thickness=DeterministicParameter('inch', 1.0),
    conductivity=DeterministicParameter('W/m/degC', 0.2),
    density=DeterministicParameter('kg/m**3', 2.7),
    specific_heat=DeterministicParameter('J / kg / degC', 0.29),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='R-5, 1 in. insulation board'
)
M16 = Layer(
    thickness=DeterministicParameter('inch', 12.0),
    conductivity=DeterministicParameter('W/m/degC', 13.50),
    density=DeterministicParameter('kg/m**3', 140.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.22),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='12 in. heavy weight concrete'
)
G01 = Layer(
    thickness=DeterministicParameter('inch', 0.625),
    conductivity=DeterministicParameter('W/m/degC', 1.11),
    density=DeterministicParameter('kg/m**3', 50.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.26),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='5/8 in. gyp board'
)
F02 = Layer(
    thickness=DeterministicParameter('inch', 0.001),
    conductivity=DeterministicParameter('W/m/degC', 0.001),
    density=DeterministicParameter('kg/m**3', 0.001),
    specific_heat=DeterministicParameter('J / kg / degC', 0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='Inside vertical surface resistance'
)
brick_wall_19_seg = Segment([F01, M01, F04, I01, M16, F04, G01, F02])
brick_wall_19 = EnvelopeSegment(
                    brick_wall_19_seg,
                    DeterministicParameter(None, 0.75),
                    'BRICK WALL 19'
)
"""
Window
------
All four walls have windows. Double glaze window of type CLR 3MM/6MM AIR
is selected. The window is modeled as a segment consisiting of 3 layers.
The relative area of window segment is 0.25.
"""
clear_3mm = Layer(
    thickness=DeterministicParameter('m', 0.003),
    conductivity=DeterministicParameter('W/m/degC', 0.9),
    density=DeterministicParameter('kg/m**3', 0, 'Value NA'),
    specific_heat=DeterministicParameter('J / kg / degC', 0, 'Value NA'),
    solar_transmittance=DeterministicParameter(None, 0.837),
    description='Window material glazing CLEAR GLASS 3MM'
)
air_6mm = Layer(
    thickness=DeterministicParameter('m', 0.006),
    conductivity=DeterministicParameter('W/m/degC', 0.024),
    density=DeterministicParameter('kg/m**3', 0, 'Value NA'),
    specific_heat=DeterministicParameter('J / kg / degC', 718, 'Value NA'),
    solar_transmittance=DeterministicParameter(None, 0.9),
    description='Air filled between panes'
)
window_seg = Segment([clear_3mm, air_6mm, clear_3mm])
window = EnvelopeSegment(
            window_seg,
            DeterministicParameter(None, 0.25),
            'Dbl Clr 3mm/6mm Air'
)
wall_segments = [brick_wall_19, window]
wall1 = Envelope(a, b, wall_segments)
wall2 = Envelope(a, b, wall_segments)
wall3 = Envelope(a, b, wall_segments)
wall4 = Envelope(a, b, wall_segments)
"""
Roof
----
Sloped frame roof type 1 provided in ASHRAE Handbook Table 17 is taken
as roof type here. The roof is modelled as a segment consisiting of 7
layers.
"""
F08 = Layer(
    thickness=DeterministicParameter('inch.', 0.03),
    conductivity=DeterministicParameter('W/m/degC', 314.0),
    density=DeterministicParameter('kg/m**3', 489.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.12),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='Metal surface'
)
G03 = Layer(
    thickness=DeterministicParameter('inch.', 0.5),
    conductivity=DeterministicParameter('W/m/degC', 0.47),
    density=DeterministicParameter('kg/m**3', 25.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.31),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='1/2 in. fiberboard sheathing'
)
F05 = Layer(
    thickness=DeterministicParameter('inch.', 0.001),
    conductivity=DeterministicParameter('W/m/degC', 0.001),
    density=DeterministicParameter('kg/m**3', 0.001),
    specific_heat=DeterministicParameter('J / kg / degC', 0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='Metal surface'
)
I05 = Layer(
    thickness=DeterministicParameter('inch.', 6.08),
    conductivity=DeterministicParameter('W/m/degC', 0.32),
    density=DeterministicParameter('kg/m**3', 1.2),
    specific_heat=DeterministicParameter('J / kg / degC', 0.23),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='R-19, 6-1/4 in. batt insulation'
)
F03 = Layer(
    thickness=DeterministicParameter('inch.', 0.001),
    conductivity=DeterministicParameter('W/m/degC', 0.001),
    density=DeterministicParameter('kg/m**3', 0.001),
    specific_heat=DeterministicParameter('J / kg / degC', 0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='Inside horizontal surface resistance'
)
roof_seg = Segment([F01, F08, G03, F05, I05, G01, F03])
roof_type1 = EnvelopeSegment(
                    roof_seg,
                    DeterministicParameter(None, 1.0),
                    'Sloped frame roof type 1'
)
roof = Envelope(a, a, roof_type1)
"""
Floor
----
Floor is modeled as a segment consisting of 4 layers.
"""
M02 = Layer(
    thickness=DeterministicParameter('inch.', 6.0),
    conductivity=DeterministicParameter('W/m/degC', 3.39),
    density=DeterministicParameter('kg/m**3', 32.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.21),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='6 in. LW concrete block'
)
I02 = Layer(
    thickness=DeterministicParameter('inch.', 2.0),
    conductivity=DeterministicParameter('W/m/degC', 0.2),
    density=DeterministicParameter('kg/m**3', 2.7),
    specific_heat=DeterministicParameter('J / kg / degC', 0.29),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='R-10, 2 in. insulation board'
)
G02 = Layer(
    thickness=DeterministicParameter('inch.', 0.625),
    conductivity=DeterministicParameter('W/m/degC', 0.8),
    density=DeterministicParameter('kg/m**3', 34.0),
    specific_heat=DeterministicParameter('J / kg / degC', 0.29),
    solar_transmittance=DeterministicParameter(None, 0.),
    description='5/8 in. plywood'
)
floor_seg = Segment([M02, I02, G02, F03])
floor_type = EnvelopeSegment(
                    floor_seg,
                    DeterministicParameter(None, 1.)
)
floor = Envelope(a, a, floor_type)
zone = Zone(wall1, wall3, wall2, wall4, roof, floor)
lat = DeterministicParameter(units='deg', value=40.42)
lon = DeterministicParameter(units='deg', value=-86.91)
alt = DeterministicParameter(units='m', value=186.0)
orientation = DeterministicParameter(units='deg', value=0)
single_zone_building = Building(lat, lon, alt, zone, orientation)
