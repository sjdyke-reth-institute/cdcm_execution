## Author: Rashi Jain 
## Date: June 24th, 2022 

from cdcm import *
#***********************************************#
#             Interior Enviornment              #
#***********************************************#

                    
extPressure = Variable(
              value = 0.0, 
              units = "atm", 
              name  = "extPressure", 
              track = True, 
              description = "Exterior Enviornment - Pressure")
              
              
airLeaKCoeff= Variable(
              value = 0.1,
              units = "atm/s", 
              name = "", 
              track = True, 
              description = "Air Leak Coefficient" 
              
              
# States                
intPressure    = State(
                 value = 1.0, 
                 units = "atm", 
                 track = True, 
                 description = "Interior Enviornment - Pressure") 
                 
intTemperature = State(
                 value = 298.0, 
                 units = "K", 
                 track = True, 
                 description = "Interior Enviornment - Tempeature") 
