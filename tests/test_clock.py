"""Test the clock.

Author:
    Ilias Bilionis

Date:
    3/15/2022
"""


from cdcm import *


if __name__ == "__main__":
    print(str(clock))
    # Simulate the clock
    dt = 0.1
    for i in range(10):
        clock.unsafe_step(dt)
        print(f"time = {clock.state['t']}")
