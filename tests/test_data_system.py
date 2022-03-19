"""Test the DataSystem class.

Author:
    Ilias Bilionis

Date:
    3/14/2022

"""

from cdcm import *
import numpy as np


if __name__ == "__main__":
    # Here are some random data
    y = np.random.randn(10)
    print(type(y[0]))
    # And here is the system
    rnd_sys = DataSystem(
        name="rnd_system",
        state=PhysicalStateVariable(value=np.float64(0.0),
                                    units="kN",
                                    name="omega",
                                    description="A random force"),
        dataset={'omega': y},
        description="Just a system with a random state."
    )
    print(str(rnd_sys))
    # The maximum number of steps allowed
    print(f"Max steps: {rnd_sys.max_num_steps}")
    # Here is how it looks
    dt = 0.1
    for i in range(rnd_sys.max_num_steps - 1):
        print(f"omega: {rnd_sys.state['omega']}")
        rnd_sys.unsafe_step(dt)
