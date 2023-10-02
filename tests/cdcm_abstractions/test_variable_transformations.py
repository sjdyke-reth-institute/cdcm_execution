"""Test transformations to Variable nodes

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


from cdcm import System, Variable
from cdcm_abstractions import scale, transform 
from cdcm_utils import make_pyvis_graph


with System(name="mysys") as mysys:

    x = Variable(name="x", value=1.0)

    # scale `x` (default name is `<var_name>_scaled`)
    x_scaled = scale(x, 10.0)

    # transform `x` (default name is `<var_name>_transformed`)
    x_transformed = transform(x, func=lambda _x: 1.0 - _x / 5.0)


print(mysys)
mysys.forward()


print(f"x.value: {x.value}, " + \
      f"x_scaled.value: {x_scaled.value}, " + \
      f"x_transformed.value: {x_transformed.value}")

g = make_pyvis_graph(mysys)
g.show("test_variable_transformations.html")