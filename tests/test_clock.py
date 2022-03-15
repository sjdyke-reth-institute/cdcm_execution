"""Test the clock.

Author:
    Ilias Bilionis

Date:
    3/15/2022
"""


from cdcm import *


if __name__ == "__main__":
    clock = Clock()
    print(clock)
    print(clock.state)
    # Simulate the clock
    dt = 0.1
    for i in range(10):
        clock.step(dt)
        print(f"time = {clock.state['t'].value:{1}.{1}}")