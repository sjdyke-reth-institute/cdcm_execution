"""An RC model for a single zone.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/20/2022

"""


from cdcm import *
import pandas as pd


df = pd.read_csv("examples/rc_system_data/weather_data_2017_pandas.csv")
data_sys = make_data_system(
    df,
    name="weather_data",
    column_units=[None, None, None, None, None, None, "degC", "Wh", "Wh"]
)

print(data_sys)

for i in range(10):
    data_sys.forward()
    print(f"Tout = {data_sys.Tout.value:1.2f}, "
          + f"Qsg = {data_sys.Qsg.value:1.2f}")
    data_sys.transition()