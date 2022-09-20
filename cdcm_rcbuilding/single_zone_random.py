"""
Example of a single zone building with uncertainty made in YABML.

Author(s):
    Sreehari Manikkan
Date:
    05/23/2022
"""
import numpy as np
from pint import UnitRegistry as ureg

from yabml import *

"""
Unit conversion factors
-----------------------
Following are the conversion factors to convert the units in British
Pound system to SI system

cf1: 1 'inch' = cf1 'm'
cf2: 1 'Btu inch / hr / foot^2 / degF' = cf2 'W / m / degC'
cf3: 1 'lb / foot^3' = cf3 'kg / m^3'
cf4: 1 'Btu / lb / degF' = cf4 'J / kg / degC'
"""
Q = ureg().Quantity
cf1 = Q(1, 'inch').to('m').magnitude
cf2 = Q(1, 'Btu inch / hr / foot^2 / degF').to('W / m / degC').magnitude
cf3 = Q(1, 'lb / foot^3').to('kg / m^3').magnitude
cf4 = Q(1, 'Btu / lb / degF').to('J / kg / degC').magnitude

a = DeterministicParameter('m', 15.0)
b = DeterministicParameter('m', 10.0)
"""
Walls
-----
Walls are made of either Brick wall type 19 or 18 given in ASHRAE
handbook Table 16. Wall area ratio is 0.75 and window area ratio is 0.25.
The wall is modeled as a segment consisting of 8 layers. The values of
parameters of layers provided are in British Pound system, but the units
are SI system as this example is for demonstration purpose.
"""
F01 = Layer(
    thickness=DeterministicParameter('m', cf1*0.001),
    conductivity=DiscreteRandomParameter('W/m/degC',
                                         cf2*np.array([0.01, 0.02]),
                                         [0.5, 0.5]
                                         ),
    density=DeterministicParameter('kg/m**3', cf3*0.001),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.001),
    solar_transmittance=DeterministicParameter(None, 0.001),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Outside surface resistance'
)
M01 = Layer(
    thickness=DeterministicParameter('m', cf1*4.0),
    conductivity=NormalRandomParameter('W/m/degC',
                                       cf2*np.array([6.2, 0.1])
                                       ),
    density=DeterministicParameter('kg/m**3', cf3*120.0),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.19),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='4 in. brick'
)
F04 = Layer(
    thickness=DeterministicParameter('m', cf1*0.001),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.001),
    density=DeterministicParameter('kg/m**3', cf3*0.001),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.001),
    solar_transmittance=DeterministicParameter(None, 0.001),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Wall air space resistance'
)
I01 = Layer(
    thickness=DeterministicParameter('m', cf1*1.0),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.2),
    density=DeterministicParameter('kg/m**3', cf3*2.7),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.29),
    solar_transmittance=DeterministicParameter(None, 0.001),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='R-5, 1 in. insulation board'
)
M16 = Layer(
    thickness=DeterministicParameter('m', cf1*12.0),
    conductivity=DeterministicParameter('W/m/degC', cf2*13.50),
    density=DeterministicParameter('kg/m**3', cf3*140.0),
    specific_heat=UniformRandomParameter('J / kg / degC',
                                         cf4*np.array([0.22, 0.25])
                                         ),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='12 in. heavy weight concrete'
)
G01 = Layer(
    thickness=LogNormalRandomParameter('m',
                                       cf1*np.array([0.625, 1e-3])
                                       ),
    conductivity=DeterministicParameter('W/m/degC', cf2*1.11),
    density=DeterministicParameter('kg/m**3', cf3*50.0),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.26),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='5/8 in. gyp board'
)
F02 = Layer(
    thickness=DeterministicParameter('m', cf1*0.001),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.001),
    density=DeterministicParameter('kg/m**3', cf3*0.001),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Inside vertical surface resistance'
)
M13 = Layer(
    thickness=DeterministicParameter('m', cf1*8.0),
    conductivity=DeterministicParameter('W/m/degC', cf2*3.70),
    density=DeterministicParameter('kg/m**3', cf3*80.0),
    specific_heat=UniformRandomParameter('J / kg / degC',
                                         cf4*np.array([0.22, 0.25])
                                         ),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='8 in. light weight concrete'
)
brick_wall_19 = [F01, M01, F04, I01, M16, F04, G01, F02]
brick_wall_18 = [F01, M01, F04, I01, M13, F04, G01, F02]
brick_wall_seg = DiscreteRandomSegment(
                    [brick_wall_19, brick_wall_18],
                    [0.7, 0.3]
)
brick_wall = EnvelopeSegment(
                    brick_wall_seg,
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
    solar_transmittance=DiscreteRandomParameter(None,
                                                [0.8, 0.9]),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Window material glazing CLEAR GLASS 3MM'
)
air_6mm = Layer(
    thickness=DeterministicParameter('m', 0.006),
    conductivity=DeterministicParameter('W/m/degC', 0.024),
    density=DeterministicParameter('kg/m**3', 0, 'Value NA'),
    specific_heat=DeterministicParameter('J / kg / degC', 718, 'Value NA'),
    solar_transmittance=DeterministicParameter(None, 0.9),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Air filled between panes'
)
window_seg = Segment([clear_3mm, air_6mm, clear_3mm])
window = EnvelopeSegment(
            window_seg,
            DeterministicParameter(None, 0.25),
            'Dbl Clr 3mm/6mm Air'
)
wall_segments = [brick_wall, window]
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
    thickness=DeterministicParameter('m', cf1*0.03),
    conductivity=DeterministicParameter('W/m/degC', cf2*314.0),
    density=DeterministicParameter('kg/m**3', cf3*489.0),
    specific_heat=UniformRandomParameter('J / kg / degC',
                                         cf4*np.array([0.12, 0.15])
                                         ),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Metal surface'
)
G03 = Layer(
    thickness=DeterministicParameter('m', cf1*0.5),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.47),
    density=DeterministicParameter('kg/m**3', cf3*25.0),
    specific_heat=LogNormalRandomParameter('J / kg / degC',
                                           cf4*np.array([0.31, 1e-3])
                                           ),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='1/2 in. fiberboard sheathing'
)
F05 = Layer(
    thickness=DeterministicParameter('m', cf1*0.001),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.001),
    density=DeterministicParameter('kg/m**3', cf3*0.001),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='Metal surface'
)
I05 = Layer(
    thickness=DeterministicParameter('m', cf1*6.08),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.32),
    density=NormalRandomParameter('kg/m**3',
                                  cf3*np.array([1.2, 0.01])
                                  ),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.23),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='R-19, 6-1/4 in. batt insulation'
)
F03 = Layer(
    thickness=DeterministicParameter('m', cf1*0.001),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.001),
    density=DeterministicParameter('kg/m**3', cf3*0.001),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.001),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
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
    thickness=DeterministicParameter('m', cf1*6.0),
    conductivity=DeterministicParameter('W/m/degC', cf2*3.39),
    density=DeterministicParameter('kg/m**3', cf3*32.0),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.21),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='6 in. LW concrete block'
)
I02 = Layer(
    thickness=DeterministicParameter('m', cf1*2.0),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.2),
    density=DeterministicParameter('kg/m**3', cf3*2.7),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.29),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='R-10, 2 in. insulation board'
)
G02 = Layer(
    thickness=DeterministicParameter('m', cf1*0.625),
    conductivity=DeterministicParameter('W/m/degC', cf2*0.8),
    density=DeterministicParameter('kg/m**3', cf3*34.0),
    specific_heat=DeterministicParameter('J / kg / degC', cf4*0.29),
    solar_transmittance=DeterministicParameter(None, 0.),
    solar_absorptance=UniformRandomParameter(None, [0.5, 0.6]),
    IHG_absorptance=UniformRandomParameter(None, [0.8, 0.9]),
    description='5/8 in. plywood'
)
floor_seg = Segment([M02, I02, G02, F03])
floor_type = EnvelopeSegment(
                    floor_seg,
                    DeterministicParameter(None, 1.)
)
floor = Envelope(a, a, floor_type)
"""
Occupant system
---------------
"""
T_p = UniformRandomParameter("degC", [25, 27], "Tp")
action_noise = DeterministicParameter("degC", 1, "action noise")
IHG_base = UniformRandomParameter(
    "W", [300, 400], "The base internal heat gain casud by occupant"
)
gamma = NormalRandomParameter(
    None, [0, 0.1], "occupancy sensitivity of the room temperature"
)
mu_heat = UniformRandomParameter(
    "W", [1, 2], "The heating mode action parameter"
)
mu_cool = NormalRandomParameter(
    "W", [1.5, 0.01], "The cooling mode action parameter"
)
T_sp_ub = UniformRandomParameter("degC", [28, 30], "T_sp_ub")
T_sp_lb = UniformRandomParameter("degC", [18, 20], "T_sp_lb")
occupant1 = Occupant(
    T_p=T_p,
    action_noise=action_noise,
    IHG_base=IHG_base,
    gamma=gamma,
    mu_heat=mu_heat,
    mu_cool=mu_cool,
    T_sp_ub=T_sp_ub,
    T_sp_lb=T_sp_lb,
    description="Occupant 1 object",
)
T_p = UniformRandomParameter("degC", [23, 26], "Tp")
action_noise = DeterministicParameter("degC", 0, "action noise")
IHG_base = UniformRandomParameter(
    "W", [350, 400], "The base internal heat gain casud by occupant"
)
gamma = NormalRandomParameter(
    None, [0, 0.3], "occupancy sensitivity of the room temperature"
)
mu_heat = UniformRandomParameter(
    "W", [1.5, 3], "The heating mode action parameter"
)
mu_cool = NormalRandomParameter(
    "W", [2, 0.01], "The cooling mode action parameter"
)
T_sp_ub = UniformRandomParameter("degC", [29, 30.5], "T_sp_ub")
T_sp_lb = UniformRandomParameter("degC", [19, 21], "T_sp_lb")
occupant2 = Occupant(
    T_p=T_p,
    action_noise=action_noise,
    IHG_base=IHG_base,
    gamma=gamma,
    mu_heat=mu_heat,
    mu_cool=mu_cool,
    T_sp_ub=T_sp_ub,
    T_sp_lb=T_sp_lb,
    description="Occupant 2 object",
)
occupants = [occupant1, occupant2]
zone = Zone(wall1, wall3, wall2, wall4,
            roof, floor, occupants
            )
lat = DeterministicParameter(units='deg', value=40.42)
lon = DeterministicParameter(units='deg', value=-86.91)
alt = DeterministicParameter(units='m', value=186.0)
orientation = DeterministicParameter(units='deg', value=0)
single_zone_building = Building(lat, lon, alt, zone, orientation)
