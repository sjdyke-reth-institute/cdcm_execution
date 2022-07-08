"""An RC model for a single zone.
Please see the complete documentation here:
https://github.com/nsf-cps-purdue/documentation/blob/main/systems/RC_model.ipynb

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/21/2022
    5/24/2022
    7/05/2022

"""


__all__ = ["RCBuildingSystem", "make_rc_of_cdcm"]


from cdcm import *
from scipy import signal
import numpy as np


class RCBuildingSystem(System):
    """An 5R3C model for a single zone.

    Arguments:

    dt              --  The timestep to use (must be a node.)
    weather_system  --  A weather system that includes:
                        Tout: outdoor air temperature
                        Qsg:  solar irradiance
                        T_gd: ground temperature
    T_cor           -- The temperature of corridor. Typically constant. It
                       can be replaced with sensor value in implemenation.
                       [C]
    Q_int           --  Internal heat gain calculated from other system
    u               -- Control variable. Input heat loads to the system.
                       [W]

    States:
    T_env           -- The surface temperature of envelope interior [C]
    T_genv          -- The surface temperature of ground envelope interior
                       [C]
    T_room          -- The room air temperature [C]

    Function nodes:
    make_matrices   -- Make ABCD discrete matrix for state space model
    transition_room -- Transition function of the states
    g_T_room_sensor -- Sensor function of adding noise to the real state

    Paramters:
    C_env           -- Capacitance of the envelope [J/C]
    C_air           -- Capacitance of the room air [J/C]
    C_genv          -- Capacitance of the ground envelope [J/C]
    R_rc            -- Thermal resistance between room and corridor [C/W]
    R_oe            -- Thermal resistance between outdoor and envelope [C/W]
    R_er            -- Thermal resistance between room and envelope [C/W]
    R_gr            -- Thermal resistance between room and ground envelope
                       [C/W]
    R_ge            -- Thermal resistance between ground envelope and ground
                       [C/W]
    a_sol_env       -- Absorptance of envelope with respect to solar irradiance
    a_sol_room      -- Absorptance of room with respect to solar irradiance
    a_IHG           -- Absorptance of room with respect to internal heat gain
    T_room_sensor_sigma -- Standard deviation of the measurement noise

    Variables:
    T_room_sensor   -- A temperature sensor at the room[C]
    A               -- Discritized State space A matrix
    B               -- Discritized State space B matrix
    """
    def define_internal_nodes(self,
                              *,
                              dt=None,
                              weather_system=None,
                              T_cor=None,
                              Q_int=None,
                              u=None,
                              **kwargs
                              ):
        # super().__init__(**kwargs)

        T_env = State(
            name="T_env",
            value=20.0,
            units="degC",
            track=True,
            description="Temperature of envelope inner surface"
        )

        T_room = State(
            name="T_room",
            value=23.0,
            units="degC",
            track=True,
            description="Temperature of room"
        )

        T_genv = State(
            name="T_genv",
            value=23.0,
            units="degC",
            track=True,
            description="Temperature of ground envelope inner surface"
        )

        C_env = Parameter(
            name="C_env",
            value=3.1996e6,
            units="J/C",
            description="Capacitance of the envelope"
        )

        C_room = Parameter(
            name="C_room",
            value=3.5187e5,
            units="J/C",
            description="Capacitance of the room air"
        )

        C_genv = Parameter(
            name="C_genv",
            value=np.inf,
            units="J/C",
            description="Capacitance of the room air"
        )

        R_rc = Parameter(
            name="R_rc",
            value=0.00706,
            units="C/W",
            description="Thermal resistance between room and corridor"
        )

        R_oe = Parameter(
            name="R_oe",
            value=0.02707,
            units="C/W",
            description="Thermal resistance between outdoor and envelope"
        )

        R_er = Parameter(
            name="R_er",
            value=0.00369,
            units="C/W",
            description="Thermal resistance between room and envelope"
        )

        R_gr = Parameter(
            name="R_gr",
            value=np.inf,
            units="C/W",
            description="Thermal resistance between room and ground envelope"
        )

        R_ge = Parameter(
            name="R_ge",
            value=0.00369,
            units="C/W",
            description="Thermal resistance between ground envelope and ground"
        )

        a_sol_env = Parameter(
            name="a_sol_env",
            value=0.90303,
            description="Absorptance of envelope with respect to solar gain"
        )

        a_sol_room = Parameter(
            name="a_sol_room",
            value=0.90303,
            description="Absorptance of room with respect to solar irradiance"
        )

        a_IHG = Parameter(
            name="a_IHG",
            value=0.90303,
            description="Absorptance of room with respect to internal heatgain"
        )

        T_gd = Variable(
            name="T_gd",
            value=18,
            units="degC",
            description="The temperature of ground. "
        )

        # u = Variable(
        #     name="u",
        #     value=0.0,
        #     description="Control of input loads to the system"
        # )

        A = Variable(
            name="A",
            value=np.zeros((3, 3)),
            description="The matrix of the dynamical system (discretized)."
        )

        B = Variable(
            name="B",
            value=np.zeros((3, 6)),
            description="The B matrix (discretized)."
        )

        @make_function(A, B)
        def make_matrices(
            dt=dt,
            R_oe=R_oe,
            R_er=R_er,
            R_rc=R_rc,
            R_gr=R_gr,
            R_ge=R_ge,
            C_room=C_room,
            C_env=C_env,
            C_genv=C_genv,
            a_sol_env=a_sol_env,
            a_sol_room=a_sol_room,
            a_IHG=a_IHG
        ):
            """Makes the dynamical system matrices and discretizes them"""
            cA = np.zeros((3, 3))
            cA[0, 0] = (-1. / C_env) * (1. / R_er + 1./R_oe)
            cA[0, 2] = 1. / (C_env * R_er)
            cA[1, 1] = (-1. / C_genv) * (1. / R_ge + 1. / R_gr)
            cA[1, 2] = 1. / (C_genv * R_gr)
            cA[2, 0] = 1. / (C_room * R_er)
            cA[2, 1] = 1. / (C_room * R_gr)
            cA[2, 2] = (-1. / C_room) * (1. / R_er + 1. / R_gr + 1. / R_rc)

            cB = np.zeros((3, 6))
            cB[0, 1] = 1./(C_env * R_oe)
            cB[0, 2] = a_sol_env / C_env
            cB[0, 3] = (1 - a_IHG) / C_env
            cB[1, 1] = 1. / (C_genv * R_ge)
            cB[2, 2] = a_sol_room / C_room
            cB[2, 3] = a_IHG / C_room
            cB[2, 4] = 1. / (C_room * R_rc)
            cB[2, 5] = 1. / C_room

            cC = np.array([[0, 0, 1]])
            cD = np.zeros(6)

            tmp = signal.StateSpace(cA, cB, cC, cD)
            discrete_matrix = tmp.to_discrete(dt=dt)
            A = discrete_matrix.A
            B = discrete_matrix.B

            return A, B

        @make_function(T_env, T_genv, T_room)
        def transition_room(
            T_env=T_env,
            T_room=T_room,
            T_genv=T_genv,
            T_cor=T_cor,
            T_gd=T_gd,
            u=u,
            dt=dt,
            A=A,
            B=B,
            # add noise for Tout, Qsg and Q_int
            T_out=weather_system.Tout,
            Q_sg=weather_system.Qsg,
            Q_int=Q_int
        ):
            """Transitions the system."""
            # print("Actual shape of A:", np.shape(A))
            res = (
                A @ np.array([T_env, T_genv, T_room]).T
                + B @ np.array([T_out, T_gd, Q_sg, Q_int, T_cor, u]).T
                # + B @ np.append([T_out, T_gd, Q_sg, Q_int, T_cor], u)
            )
            return res[0], res[1], res[2]

        T_room_sensor = Variable(
            name="T_room_sensor",
            units="degC",
            value=23.0,
            description="A temperature sensor at the room"
        )

        T_room_sensor_sigma = Parameter(
            name="T_room_sensor_sigma",
            units="degC",
            value=0.01,
            description="Standard deviation of the measurement noise"
        )

        @make_function(T_room_sensor)
        def g_T_room_sensor(
            T_room=T_room,
            T_room_sensor_sigma=T_room_sensor_sigma
        ):
            """Get a sensor measurement."""
            return T_room + T_room_sensor_sigma * np.random.randn()


def make_rc_of_cdcm(zone, neighbor, dt, weather_sys, T_cor, Q_int, u_t, name):
    """
    Makes an RC CDCM system corresponding to the YABML zone given.

    Arguments:
        zone    --  A zone object of the building. Its an instance of the Zone
                    class in YABML.
        neighbor    --  neighbor list of the zone provided. Its a list.
        dt  --  The timestep to use (must be a node.)
        weather_system  --  A weather system that includes:
                            Tout: outdoor air temperature
                            Qsg:  solar irradiance
                            T_gd: ground temperature
        T_cor   -- The temperature of corridor. Typically constant. It
                        can be replaced with sensor value in implemenation.
                        [C]
        Q_int   --  Internal heat gain calculated from other system
        u_t     -- Control variable. Input heat loads to the system.
                        [W]
        name    -- name of the RCBuildingSystem object to be created. It is a
                string. 

    """
    R_list = []
    C_list = []
    trans_list = []
    Area_list = []
    cp_air = 1006  # J/Kg-C
    rho_air = 1.2  # Kg/m^3
    x = zone.edges[0].lx.value
    z = zone.edges[0].ly.value
    y = zone.edges[1].lx.value
    V = x * y * z
    Cp_room = V * rho_air * cp_air

    for e in zone.edges:
        lx = e.lx.value
        ly = e.ly.value
        Area = lx * ly
        Area_list.append(Area)
        U = 0
        C = 0
        sub_trans_list = []

        for seg in e.segments:
            area_ratio = seg.relative_area.value
            # indicator for whether the layer is transparent
            solar_trans = 1
            r = 0
            c = 0

            for layer in seg.segment.layers:
                thickness = layer.thickness.value
                conductivity = layer.conductivity.value
                density = layer.density.value
                specific_heat = layer.specific_heat.value
                solar_transmittance = layer.solar_transmittance.value
                # if one layer is not transparent,the segment is not
                # transparent
                solar_trans = min(solar_trans, solar_transmittance)

                # calculate R and C for layers
                r += thickness / conductivity
                c += thickness * density * specific_heat
            U += 1 / (r / (area_ratio * Area))
            C += c * area_ratio * Area
            sub_trans_list.append(solar_trans)

        R_list.append(1 / U)
        C_list.append(C)
        trans_list.append(sub_trans_list)

    # check nodal condition and return corresponding RC model
    out = True
    ground = False
    cor = False

    if neighbor[5] == 0:
        # the model has ground node
        ground = True

    if not all(v == 0 for v in neighbor):
        cor = True

    if all(v != 0 for v in neighbor[0:5]):
        out = False

    # Setup 5R3C model parameter placeholders
    R_oe = 0
    Cp_env = 0
    R_er = 0
    R_gr = 0
    R_ge = 0
    Cp_genv = 0
    R_rc = 0

    # By checking out, ground, cor, set RC model accordingly
    if out is False:
        Cp_env = np.inf
        R_gr = np.inf
    else:
        for i in range(5):
            if neighbor[i] == 0:
                # add the R and C of all exterior surfaces except floor
                R_oe += 1 / R_list[i]
                Cp_env += C_list[i]
                R_er += 0.87 * 5.678 / Area_list[i]  # film coefficeint
        R_oe = 1 / R_oe

    # 3R2C case
    if ground is False:
        Cp_genv = np.inf
        R_gr = np.inf
        R_ge = np.inf
    else:
        Cp_genv = C_list[5]
        R_gr += 0.87 * 5.678 / Area_list[5]
        R_ge = R_list[5]

    if cor is True:
        for i in range(6):
            if neighbor[i] != 0:
                # add the R
                R_rc += 1 / R_list[i]
                R_rc += 0.87 * 5.678 / Area_list[i]  # film coefficeint.
        R_rc = 1 / R_rc
    else:
        R_rc = np.inf

    with RCBuildingSystem(
        dt=dt,
        weather_sys=weather_sys,
        T_cor=T_cor,
        Q_int=Q_int,
        u=u_t,
        name=name,
    ) as zone_rc_sys:
        """
        we parse the information from YABML to CDCM system by setting
        the values of C and R parameters of CDCM RC system with the values
        we obtained.
        """
        zone_rc_sys.C_room.value = Cp_room
        zone_rc_sys.C_env.value = Cp_env
        zone_rc_sys.C_genv.value = Cp_genv
        zone_rc_sys.R_rc.value = R_rc
        zone_rc_sys.R_oe.value = R_oe
        zone_rc_sys.R_er.value = R_er
        zone_rc_sys.R_gr.value = R_gr
        zone_rc_sys.R_ge.value = R_ge
        return zone_rc_sys
