Tutorial
========
In this tutorial, creating a system with two sub-systems will be demonstrated.

System of Systems
^^^^^^^^^^^^^^^^^

 As it can be noticed from ``_system.py``, a system has a name, state, parameters, parents, sub-systems, and its description. Descriptions of each argument are shown below:

   * :guilabel:`name`         -- A name for the system.
   * :guilabel:`state`        -- The states of the system. A dictionary the keys of which are strings and the values are ``PhysicalStateVariable`` or ``HealthStateVariable``.
   * :guilabel:`parameters`   -- The parameters of the system. A dictionary the keys of which are strings and the values are ``Parameter``.

   * :guilabel:`parents`      -- A dictionary of keys which are strings and values that are tuples of type ``System`` or of type ``(str, System)``. In any case, the keys correspond the name of the input variable used locally by this object. For the values the story is as follows. If the value is just a ``System`` object, then we assume that this object has a state with the same name as the corresponding key. If the value is ``(str, System)``, then we assume that the first item of the tupe is the name of the input variable in the ``System`` object. Here is an example:

   .. code-block:: python

      parents = {
            "input_var_1": system_object_1,
            "input_var_2": ("foo", system_object_2)
      }


   This is a dictionary with two items. The first item tells us that there is an input named ``input_var_1``  which can be found in the object ``system_object_1``. That is, the variable can be accessed through ``system_object_1.state["input_var_1"]``. The second item, tells us that there is another input, which we name ``input_var_2``, that actually corresponds to a state called "foo" in ``system_object_2``. It can be accessed through ``system_object_2.state["foo"]``.

   Despite accepting both kinds of parents, the class using the second type of specification to store things locally because it is more general. So, the first item becomes ``input_var_1": ("input_var_1", system_object_1)`` in the internal representation.

   Now when you inherit from this class, you can access these input variables from the ``get_parent()`` method by just providing the local name.

   * :guilabel:`sub_systems`   -- A dictionary of systems. The keys must be strings. The values must be ``System``. Alternatively, a list of systems.

   * :guilabel:`description`   -- A description for the system.


PhysicalStateVariable and HealthStateVariable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These are the states of a system that represent physical and health states. More details about their structure can be found in ``/cdcm/_quantity.py``. They have: 

   * :guilabel:`value`        -- The value of the quantity. Must be an int, a double or a numpy array of ints or floating point numbers. We also allow it to be a string.
   * :guilabel:`units`        -- Must be a string or a pint object that describes an SI physical unit.   
   * :guilabel:`name`         -- A string. The name of the quantity. 
   * :guilabel:`track`        --  A boolean. If True the quantity will be tracked during simulations. If False it will not be tracked.
   * :guilabel:`description`  -- A desciption of the quantity. 

Here is an example for a state of the system:  

   .. code-block:: python

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

Parameters
^^^^^^^^^^

Parameter represents a parameter of the system and its structure is very similar to the state variables. Here is an example for it: 

   .. code-block:: python

        parameters = Parameter(value=1.2,
                               units="meters / second",
                               name="rate_of_change",
                               description="The rate of change.")

Example of a Coupled System
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we will create a system with two sub-systems. The full example can be found in ``/tests/test_coupled_system_from_function.py``. The subsytems are named :guilabel:`sys1` and :guilabel:`sys2` respectively. Each sub-system will have its own states and parameters. We will create each sub-system and combine them in the system by assigning the :guilabel:`sys1` to be a parent of the second one. Here is how :guilabel:`sys1` is created: 

.. literalinclude:: ../../tests/test_coupled_system_from_function.py
   :language: python
   :caption: *sys1*
   :lines: 13-35


Now, let us create :guilabel:`sys2`. It can be noticed that :guilabel:`sys1` is assigned as a parent sub-system:

.. literalinclude:: ../../tests/test_coupled_system_from_function.py
   :language: python
   :caption: *sys2*
   :lines: 37-66


Now let us combine both sub-systems under one system: 

.. literalinclude:: ../../tests/test_coupled_system_from_function.py
   :language: python
   :caption: *combined_system*
   :lines: 68-73

Let's run it in ten steps: 

.. literalinclude:: ../../tests/test_coupled_system_from_function.py
   :language: python
   :caption: *10-step run*
   :lines: 76-83



The whole code can be accessed from ``/tests/test_coupled_system_from_function.py`` or below: 

.. literalinclude:: ../../tests/test_coupled_system_from_function.py
   :language: python
   :caption: *Coupled System*
   :lines: 13-83

Example of a Doubly Coupled System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we will create a system with two sub-systems. The full example can be found in ``/tests/test_doubly_coupled_systems.py``. The subsytems are named :guilabel:`sys1` and :guilabel:`sys2` respectively. Each sub-system will have its own states and parameters. We will create each sub-system and combine them in the system by assigning the :guilabel:`sys1` to be a parent of the second one. Here is how :guilabel:`sys1` is created: 

.. literalinclude:: ../../tests/test_doubly_coupled_systems.py
   :language: python
   :caption: *sys1*
   :lines: 13-28


Now, let us create :guilabel:`sys2`. It can be noticed that :guilabel:`sys1` is assigned as a parent sub-system:

.. literalinclude:: ../../tests/test_doubly_coupled_systems.py
   :language: python
   :caption: *sys2*
   :lines: 29-44


Now let us combine both sub-systems under one system: 

.. literalinclude:: ../../tests/test_doubly_coupled_systems.py
   :language: python
   :caption: *combined_system*
   :lines: 44-58

Let's run it in ten steps: 

.. literalinclude:: ../../tests/test_doubly_coupled_systems.py
   :language: python
   :caption: *10-step run*
   :lines: 60-65


The whole code can be accessed from ``/tests/test_doubly_coupled_systems.py`` or below: 

.. literalinclude:: ../../tests/test_doubly_coupled_systems.py
   :language: python
   :caption: *Doubly Coupled System*
   :lines: 13-65