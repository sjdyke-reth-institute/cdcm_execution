# CDCM Code Reconfiguration

The following tutorial demonstrates creating a sustem with sub-systems. The same tutorial can be accessed in ``/docs/build/html/index.html`` prebuilt documentation. 

Tutorial
========
In this tutorial, creating a system with two sub-systems will be demonstrated.

### System of Systems

 As it can be noticed from ``_system.py``, a system has a name, state, parameters, parents, sub-systems, and its description. Descriptions of each argument are shown below:

   * `name`         -- A name for the system.
   *  `state`        -- The states of the system. A dictionary the keys of which are strings and the values are ``PhysicalStateVariable`` or ``HealthStateVariable``.
   * `parameters`   -- The parameters of the system. A dictionary the keys of which are strings and the values are ``Parameter``.

   * `parents`      -- A dictionary of keys which are strings and values that are tuples of type ``System`` or of type ``(str, System)``. In any case, the keys correspond the name of the input variable used locally by this object. For the values the story is as follows. If the value is just a ``System`` object, then we assume that this object has a state with the same name as the corresponding key. If the value is ``(str, System)``, then we assume that the first item of the tupe is the name of the input variable in the ``System`` object. Here is an example:

            parents = {
                  "input_var_1": system_object_1,
                  "input_var_2": ("foo", system_object_2)
            }


   This is a dictionary with two items. The first item tells us that there is an input named ``input_var_1``  which can be found in the object ``system_object_1``. That is, the variable can be accessed through ``system_object_1.state["input_var_1"]``. The second item, tells us that there is another input, which we name ``input_var_2``, that actually corresponds to a state called "foo" in ``system_object_2``. It can be accessed through ``system_object_2.state["foo"]``.

   Despite accepting both kinds of parents, the class using the second type of specification to store things locally because it is more general. So, the first item becomes ``input_var_1": ("input_var_1", system_object_1)`` in the internal representation.

   Now when you inherit from this class, you can access these input variables from the ``get_parent()`` method by just providing the local name.

   * `sub_systems`   -- A dictionary of systems. The keys must be strings. The values must be ``System``. Alternatively, a list of systems.

   * `description`   -- A description for the system.


### PhysicalStateVariable and HealthStateVariable

These are the states of a system that represent physical and health states. More details about their structure can be found in ``/cdcm/_quantity.py``. They have: 

   * `value`        -- The value of the quantity. Must be an int, a double or a numpy array of ints or floating point numbers. We also allow it to be a string.
   * `units`        -- Must be a string or a pint object that describes an SI physical unit.   
   * `name`         -- A string. The name of the quantity. 
   * `track`        --  A boolean. If True the quantity will be tracked during simulations. If False it will not be tracked.
   * `description`  -- A desciption of the quantity. 

Here is an example for a state of the system:  



        state = [
            PhysicalStateVariable(
                value=0.1,
                units="meters",
                name="x1",
                track=True,
                description="The x1 variable."
            ),
            HealthStateVariable(
                value=0,
                units=None,
                name="h",
                track=True,
                description="The h variable."
            )
        ]

### Parameters


Parameter represents a parameter of the system and its structure is very similar to the state variables. Here is an example for it: 



        parameters = Parameter(value=1.2,
                               units="meters / second",
                               name="rate_of_change",
                               description="The rate of change.")

### Example of a System with Two Sub-systems


In this example, we will create a system with two sub-systems. The full example can be found in ``/scripts/system_of_systems.py``. The subsytems are named :guilabel:`system_1` and :guilabel:`system_2` respectively. Each sub-system will have its own states and parameters. We will create each sub-system and combine them in the system by assigning the :guilabel:`system_1` to be a parent of the second one. Here is how :guilabel:`system_1` is created: 

    class Sys1(System):

        def __init__(self):
            name = "system_1"
            state = [
                PhysicalStateVariable(
                    value=0.1,
                    units="meters",
                    name="x1",
                    track=True,
                    description="The x1 variable."
                ),
                HealthStateVariable(
                    value=0,
                    units=None,
                    name="h",
                    track=True,
                    description="The h variable."
                )
            ]
            parameters = Parameter(value=1.2,
                                   units="meters / second",
                                   name="rate_of_change",
                                   description="The rate of change.")
            super().__init__(
                name=name,
                state=state,
                parameters=parameters,
                description="A simple system."
            )


Now, let us create :guilabel:`system_2`. It can be noticed that :guilabel:`system_1` is assigned as a parent sub-system:


    class Sys2(System):

        def __init__(self, sys_1):
            name = "system_2"
            state = PhysicalStateVariable(
                value=0.3,
                units="meters",
                name="x2",
                track=True,
                description="The x2 variable."
            )
            parameters = [
                Parameter(
                    value=1.2,
                    units="meters / second",
                    name="rate_of_change_2",
                    description="The rate of change 2."
                ),
                Parameter(
                    value=0.1,
                    units="1 / second",
                    name="coupling_coeff",
                    description="Coupling coeff."
                )
            ]
            parents = {'x1': sys_1}
            super().__init__(
                name=name,
                state=state,
                parameters=parameters,
                parents=parents,
                description="Another simple system."
            )


Now let us combine both sub-systems under one system: 

     # Create the systems
        sys1 = Sys1()
        sys2 = Sys2(sys1)
        # Put them in a system of system container
        sys = System(
            name="combined_system",
            sub_systems=[sys1, sys2]
        )
        print(sys)


The whole code can be accessed from ``/tests/test_simple_system_of_systems.py``
