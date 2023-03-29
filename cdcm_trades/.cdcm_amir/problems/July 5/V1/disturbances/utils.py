"""Some utility functions."""


__all__ = ["is_loonar_day"]


def is_loonar_day(t, half_day_light):
    """
    Check if it is loonar day or night.

    Assumes that day starts at t = 0.
    """
    return t % (2 * half_day_light) < half_day_light
