"""A clas representing a power distribution system.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


from . import System


class PowerDistributionSystem(System):
    """A power distribution system.

    A power distribution system connects power generator systems
    (`PowerGenerator`) to power consumer (`PowerConsumer`) and power
    storage (`PowerStorage`) systems.

    TODO: We haven't thought yet about `PowerStorage`.

    The `power_output` state of each generator is a parent of the
    distribution system. This parent should be uniquely named.

    The `required_power` of each consumer is a parent of the
    `PowerDistributionSystem`. This parent should be uniquly named.

    For each connected power consumer, the distribution system
    should have a state that indicates how much power is available to
    that power consumer during the next timestep.

    Keyword Arguments:

    See `System` for the definition of the keyword arguments.
    """

    def __init__(
        name="power_disribution",
        description=""
    ):
        pass
