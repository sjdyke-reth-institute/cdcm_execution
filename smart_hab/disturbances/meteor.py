"""An METEOR model."""



__all__ = ["make_meteor_env_0"]



from cdcm import *
import math
import numpy as np


def make_meteor_env_0(clock, moon, dome_specs):
    with System(name="meteor", description="The meteor environment") as meteor:
        meteor_hit_rate = Parameter(
            name="meteor_hit_rate",
            value=15 / 1000 / 3600,
            units="1/sec",
            description="rate of meteor hitting the dome"
        )

        meteor_impacts_1 = Variable(
            name="meteor_impacts_1",
            value=0.0,
            units="",
            description="Meteor damage on Dome section 1"
        )
        meteor_impacts_2 = Variable(
            name="meteor_impacts_2",
            value=0.0,
            units="",
            description="Meteor damage on Dome section 2"
        )
        meteor_impacts_3 = Variable(
            name="meteor_impacts_3",
            value=0.0,
            units="",
            description="Meteor damage on Dome section 3"
        )
        meteor_impacts_4 = Variable(
            name="meteor_impacts_4",
            value=0.0,
            units="",
            description="Meteor damage on Dome section 4"
        )
        meteor_impacts_5 = Variable(
            name="meteor_impacts_5",
            value=0.0,
            units="",
            description="Meteor damage on Dome section 5"
        )

        print(type(moon), type(dome_specs))
        @make_function(meteor_impacts_1,
                       meteor_impacts_2,
                       meteor_impacts_3,
                       meteor_impacts_4,
                       meteor_impacts_5)
        def f_meteor_impacts(dome_surface_area=dome_specs.dome_surface_area,
                             meteor_hit_rate=meteor_hit_rate,
                             meteor_samp_location=moon.meteor_samp_location,
                             meteor_samp_impact=moon.meteor_samp_impact,
                             dt=clock.dt):
            """Transition function for meteor_impacts"""
            meteor_impacts_new = ([0.0, 0.0, 0.0, 0.0, 0.0])
            P_collide_based_on_dome_size = min(max(dome_surface_area /
                                                   (2 * math.pi *
                                                    math.power(20, 2)), 0.5), 1)
            p_hit = np.random.random()
            if p_hit < meteor_hit_rate * P_collide_based_on_dome_size * dt:
                p_choice = np.random.randint(10000)
                location_hit = int(meteor_samp_location[p_choice] + 1)
                meteor_impacts_new[location_hit - 1] = \
                    meteor_samp_impact[p_choice]

            return meteor_impacts_new[0], \
                   meteor_impacts_new[1], \
                   meteor_impacts_new[2], \
                   meteor_impacts_new[3], \
                   meteor_impacts_new[4]

    return meteor
