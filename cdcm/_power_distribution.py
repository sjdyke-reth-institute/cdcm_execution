"""A clas representing a power distribution system.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


from . import System, PowerGenerator, PowerConsumer


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
        self,
        name="power_disribution",
        state={},
        parameters={},
        parents={},
        sub_systems={},
        description=""
    ):
        super().__init__(
            name=name,
            description=description,
            state=state,
            parameters=parameters,
            parents=parents,
            sub_systems=sub_systems
        )
        self._generator_names = []
        self._consumer_names = []

    @property
    def generator_names(self):
        """Get the names of the parents that are generators."""
        return self._generator_names

    @property
    def consumer_names(self):
        """Get the names of the parents that are consumers."""
        return self._consumer_names

    def add_generator(self, system, generator_name=None):
        """Adds a generator to the distribution network.

        Arguments:
        system     -- The `PowerGenerator` system to connect.

        Keyword Arguments
        generator_name -- The name used to refer to this power
                          generator. If not specified, then
                          we use "power_input_<count>" where <count>
                          starts from zero and counts the number of
                          generators added so far.
        """
        assert isinstance(system, PowerGenerator)
        if generator_name is None:
            generator_name = f"power_input_{len(self.generator_names)}"
        self.add_parent(generator_name, system, "power_output")

    @property
    def power_in(self):
        """Get the total power generated during this timestep."""
        s = 0.0
        for g_name in self.generator_names:
            s += self.get_parent_state(g_name).value
        return s

    def add_consumer(self, system, consumer_name=None):
        """Adds a consumer to the distribution network.

        Arguments:
        system     -- The `PowerConsumer` system to connect.

        Keyword Arguments
        consumer_name -- The name used to refer to this power
                          consumer. If not specified, then
                          we use "power_output_<count>" where <count>
                          starts from zero and counts the number of
                          generators added so far.
        """
        assert isinstance(system, PowerConsumer)
        if consumer_name is None:
            consumer_name = f"power_output_{len(self.consumer_names)}"
        self.add_parent(consumer_name, system, "required_power")

    @property
    def required_power(self):
        """Get the total power required during this timestep."""
        s = 0.0
        for c_name in self.consumer_names:
            s += self.get_parent_state(c_name).value
        return s
