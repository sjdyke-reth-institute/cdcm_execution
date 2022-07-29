from cdcm import *
import numpy as np
from typing import Union

with System(name="human_agent",
    description="A naive human agent model.") as human_agent:
    clock = make_clock(dt=1, units="hrs")

    with System(name="resources",
        description="Resources input and output of human agent.") as resources:

        with System(name="oxygen",
            description="Oxygen input and output of human agent.") as oxygen:

            oxygen_consumption = Variable(
                value=0.0,
                units="kg",
                name="oxygen_consumption",
                track=True,
                description="The oxygen consumed by human agent in a time step."
            )
            @make_function(oxygen_consumption)
            def calculate_oxygen_consumption(t=clock.t):
                value = 1*t
                return value
            oxygen_power = Variable(
                value=0.0,
                units="W",
                name="oxygen_power",
                track=True,
                description="The power consumed by oxygen regeneration device in a time step."
            )
            @make_function(oxygen_power)
            def calculate_oxygen_power(o_c=oxygen_consumption):
                value = 2*o_c
                return value

        with System(name="water",
            description="Water input and output of human agent.") as water:
            pass

        with System(name="food",
            description="Food input and output of human agent.") as food:
            pass

    with System(name="physical_location",
        description="Pysical location of human agent.") as physical_location:
        room_id = Variable(
            value=0,
            units="",
            name="room_id",
            track=True,
            description="The id of the room human agent is in in this time step."
        )
        def map_neighbour(r_i):
            # for distance in distance_map: if distance is 1, add to r_i_neighbour
            r_i_neighbour = [0]
            return r_i_neighbour
        @make_function(room_id)
        def calculate_physical_location():
            # r_i_candidate = map_neighbour(r_i)
            # r_i = human_action(r_i_candidate,)
            r_i = room_id
            return r_i

    with System(name="heat_transfer",
        description="Heat transfer output of human agent.") as heat_transfer:
        heat_output = Variable(
            value=0,
            units="J",
            name="heat_output",
            track=True,
            description="The heat output of human agent."
        )
        @make_function(heat_output)
        def calculate_heat_output(t=clock.t):
            value = 1*t
            return t

print(human_agent)

for i in range(10):
    human_agent.forward()

    print(f"t = {human_agent.clock.t.value:1.1f},\
        oxygen consumption = {human_agent.resources.oxygen.oxygen_consumption.value:1.1f},\
        oxygen power = {human_agent.resources.oxygen.oxygen_power.value:1.1f}")

    human_agent.transition()
