
Comments on the code:

# 7 - 27 - 2022
Physical_object should be able to take in area as well. For some objects such
as solar panels. We may want to size them according to the mission. In that
case we'd want to be able to take area and output length_x, and length_y just
like we did it in case of mass and volume.

With specific components: sequential_shunt_unit, I'd like to be able to create
i units of that specific component as a system, and be able to assign it an ID

Comment:
Currently I've categorized the whole solar arrays as one system. But I think,
a better idea would be to have what we want to have for sequential_shunt_units.
This would allow us to play with configuration a little bit. While my goal for
year 1 is to have a basic functioning habitat (that includes some if not most)
elements. The goal for year 4 would be to play around with the scale of the habitat.
In different architectures and configurations.

Establishing connections. For example, each DCSU is linked to a set number of
BCDU's or batteries. RPCM Connections to Power Loads... etc.



This week: Finish coding power system and abstractions.
Next week: Move to establishing connections
Week after next: Include disturbances to power system
                 Systems that need to be modeled in power systems.
Following weeks: Unit testing
                 Establishing database for power systems