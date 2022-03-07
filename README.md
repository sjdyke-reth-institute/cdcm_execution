# CDCM_reconfig

Here is the example of the system. Data classes in Python are to be used:  


    System:
  
    Data: 
        current_state
        inputs = [sys1: ["in1", "in2"],
                  sys2: ["in3", "in4"]]
        next_state 
    
    Methods:
        step(dt)
        transition() (curr_state=next_state)
        
    SolarIrSys:
        current_state = [SolIr]
        next_state 
        step(dt):
            read_from_file
        inputs = None
        transition()
        
    SolarPanelSys:
        current_state = [pacd, power]
        inputs = [solarIr: "solar_ir",
                  dustProc: "dust"]
        step(dt):
            sol = input[...]
            dust = input[...]
            power = f(solar, dust)
            pacd = f(...,...)
        transition()
    SensorPower:
        current_state = [MsPower]
        inputs = SolarPanels.power
        step(dt)


The following blocks are the examples of defining state with its parameters: 
        
    Static Parameter: 
        units (pint)
        description (String)
        value (np.array)
        name

    State: 
        name
        units
        description
        is.observed
        is.traded
