

## Functionality construction
```python
Scalar = Union[int, float]

class Functionality(Variable):
    """Functionality variable"""
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name=name, **kwargs)


def make_functionality(functionality_name: str, **kwargs):
    """A function that creates a functionality variable with a health status depdnency"""
    
    def make_functionality_wrapper(func: Callable) -> Functionality:
        """Wrapper procedure defining a `Functionality` node and a `Function`
        node.
        
        Arguments
        ---------
        func        :   Callable
            A function that defines how to set the value of the functionality variable
        """

        signature = get_default_args(func)
        parents = signature.values()

        assert not hasattr(System.get_context(), functionality_name)

        functionality = Functionality(
            name=functionality_name,
            value=0.,
            description="Functionality of the system"
        )
        fn_func_var = Function(
            name=func.__name__,
            children=functionality,
            parents=parents,
            func=func,
            description=f"Procedure that sets the value of {functionality.absname}"
        )
        return fn_func_var 
    
    return make_functionality_wrapper
```

## Functionality Usage
```python
from cdcm import *
from cdcm_abstractions import *
from cdcm_utils import *

with System(name="system") as sys:

    clock = make_clock(dt=1.0, units="hr")

    hvar1 = make_health_variable(
        name="health_variable",
        value=0.,
        description="A health variable of the system"
    )
    rate = Parameter(
        name="rate",
        value=0.1,
        description="Rate of a flow"
    )

    @make_functionality("func_flow")
    def fn_func_hvar1(hvar=hvar1, rate=rate, dt=clock.dt):
        """Calculate functionality from variables"""
        if hvar == 0:
            return 2. * rate * dt
        else:
            return rate * dt

print("~ovn!")        
print(sys)

sys.forward()

print("~~ovn!")

sys_graph = make_pyvis_graph(sys, "test_functionality.html")

```

