"""An RC model for a single zone.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/21/2022

"""


__all__ = ["RCBuildingSystem"]


from cdcm import *
from functools import lru_cache
from scipy import signal
import numpy as np


class RCBuildingSystem(System):
    """An 3R2C model for a single zone.

    Arguments

    dt              --  The timestep to use (must be a node.)
    weather_system  --  A weather system that includes Tout, Qsg,
                        and Qint.

    T_env           -- The surface temperature of envelope interior
    T_room          -- The room air temperature

    C_env           -- Capacitance of the envelope
    C_air           -- Capacitance of the room air
    R_rc            -- Thermal resistance between room and corridor
    R_oe            -- Thermal resistance between outdoor and envelope
    R_er            -- Thermal resistance between room and envelope

    a_sol_env       -- Absorptance of envelope with respect to solar irradiance

    T_cor           -- The temperature of corridor. Typically constant. It
                       can be replaced with sensor value in implemenation.
    u               -- Control variable. Input heat loads to the system.
    """
    def __init__(self,
                 dt: Parameter,
                 weather_system: System,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        T_env = State(
            name="T_env",
            value=20.0,
            units="degC",
            track=True,
            description="Temperature of envelope"
        )

        T_room = State(
            name="T_room",
            value=23.0,
            units="degC",
            track=True,
            description="Temperature of room"
        )

        C_env = Parameter(
            name="C_env",
            value=3.1996e6,
            units="W/C",
            description="Capacitance of the envelope"
        )

        C_air = Parameter(
            name="C_air",
            value=3.5187e5,
            units="W/C",
            description="Capacitance of the room air"
        )

        R_rc = Parameter(
            name="R_rc",
            value=0.00706,
            units="J/W",
            description="Thermal resistance between room and corridor"
        )

        R_oe = Parameter(
            name="R_oe",
            value=0.02707,
            units="J/W",
            description="Thermal resistance between outdoor and envelope"
        )

        R_er = Parameter(
            name="R_er",
            value=0.00369,
            units="J/W",
            description="Thermal resistance between room and envelope"
        )

        a_sol_env = Parameter(
            name="a_sol_env",
            value=0.90303,
            description="Absorptance of envelope with respect to solar irradiance"
        )

        A = Variable(
            name="A",
            value=np.zeros((2, 2)),
            description="The matrix of the dynamical system (discretized)."
        )

        B = Variable(
            name="B",
            value=np.zeros((2, 5)),
            description="The B matrix (discretized)."
        )

        @make_function(A, B)
        def make_matrices(
            dt=dt,
            C_env=C_env,
            C_air=C_air,
            R_er=R_er,
            R_oe=R_oe,
            R_rc=R_rc,
            a_sol_env=a_sol_env
        ):
            """Makes the dynamical system matrices and discretizes them"""
            cA = np.zeros((2, 2))
            cA[0, 0] = (-1. / C_env) * (1. / R_er + 1./R_oe)
            cA[0, 1] = 1. / (C_env * R_er)
            cA[1, 0] = 1. / (C_air * R_er)
            cA[1, 1] = (-1. / C_air) * (1. / R_er + 1. / R_rc)

            cB = np.zeros((2, 5))
            cB[0, 1] = 1./(C_env * R_oe)
            cB[0, 2] = a_sol_env / C_env
            cB[1, 0] = 1. / (C_air * R_rc)
            cB[1, 2] = (1. - a_sol_env) / C_air
            cB[1, 3] = 1. / C_air
            cB[1, 4] = 1. / C_air

            cC = np.array([[1, 0]])
            cD = np.zeros(5)

            tmp = signal.StateSpace(cA, cB, cC, cD)
            discrete_matrix = tmp.to_discrete(dt=dt)
            A = discrete_matrix.A
            B = discrete_matrix.B

            return A, B

        T_cor = Parameter(
            name="T_cor",
            value=23,
            units="degC",
            description="The temperature of corridor."
        )

        u = Variable(
            name="u",
            value=0,
            description="Control of input loads to the system"
        )

        @make_function(T_env, T_room)
        def transition(
            T_env=T_env,
            T_room=T_room,
            A=A,
            B=B,
            T_cor=T_cor,
            u=u,
            T_out=weather_system.Tout,
            Q_sg=weather_system.Qsg,
            Q_int=weather_system.Qint
        ):
            """Transitions the system."""
            res = (
                A @ [T_env, T_room]
                + B @ np.append([T_cor, T_out, Q_sg, Q_int], u)
            )
            return res[0], res[1]

        self.add_nodes([
                T_env, T_room,
                C_env, C_air,
                R_rc, R_oe, R_er, a_sol_env,
                A, B, u, make_matrices,
                transition
            ]
        )