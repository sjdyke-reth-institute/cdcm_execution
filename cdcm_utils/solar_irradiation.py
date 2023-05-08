#~ovn!
"""Stoachstic irradiation model

Author:
    Sreehari Manikkan
    R Murali Krishnan
Date:
    02.20.2023
    05.08.2023
    
"""


import requests
import re
import math
import pandas as pd
import numpy as np


__all__=["get_insolation_ephemeris"]


def get_data_from_jplh(
        start_time: str,
        end_time: str,
        step_size: str,
        quantities: str,
        target: str,
        observe_body: str,
        phi=0.,
        lamda=0.,
        altitude=0.,
    
):     
    """Arguments:
        start_time: A string containing the start time in the format
                    supported by JPL Horizon.
        end_time: A string containing the end time in the format
                  supported by JPL Horizon.
        step_size: A string containing the step size of time in
                   the format supported by JPL Horizon.

        quantities: A string containing the numbers corresponding to
                    the quantities available in the JPL Horizon.
        target: target body code specified by JPL Horizon. It is a string.
        observe_body: observer location codeas specified by JPL Horizon.
                      It is a string.
        (Refer below link for more details on above arguments:
        https://ssd.jpl.nasa.gov/horizons/manual.html#intro
        )

        Return:
         data: list containing the data as string elements.
    """
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    url += "?format=text&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'"
    if quantities == '19':
        url += f"&COMMAND='{target}'&CENTER='500@{observe_body}'&START_TIME='{start_time}'&STOP_TIME='{end_time}'&STEP_SIZE='{step_size}'&QUANTITIES='{quantities}'"
    elif quantities == '4':
        url += f"&COMMAND='{target}'&CENTER='coord@{observe_body}'&START_TIME='{start_time}'&COORD_TYPE='GEODETIC'&SITE_COORD='{lamda},{phi},{altitude}'&STOP_TIME='{end_time}'&STEP_SIZE='{step_size}'&QUANTITIES='{quantities}'"
    else:
        raise Exception("invalid quantity specified")
    response = requests.get(url)
    result = response.text
    # https://stackoverflow.com/questions/33312175/matching-any-character-including-newlines-in-a-python-regex-subexpression-not-g/33312193#33312193
    # https://ideone.com/GZEQNf
    data = re.findall(r"\$\$SOE(?s:.*?)\$\$EOE.*", result, re.M)
    data = re.split("\n", data[0])
    return data


def to_float(df, columns):
    """
    Converts the given column of pandas df to float.
    
    Arguments:
        df: pandas dataframe
        columns: List of columns as strings.
    """
    for column in columns:
        df[column] = df[column].astype(float)

def get_solar_irradiance(
        Rm=0.,
        solar_azimuth=0.,
        elevation=0.,
        phi=0.,
        lamda=0.,
        alpha=0.,
        beta=0.
    ):
    """
    Get the value of solar irradiance on the Moon.
    
    Arguments:
        Rm - Distance between Sun and Moon at the given time in AU. Its a float.\
        solar_azimuth - solar azimuth angle in degrees. 
            North(0) -> East(90) -> South(180) -> West(270) -> North (360)
        elevation: elevation angle of sun in degrees. (-90 to +90) 
        phi - Latitude of the location at the Moon where solar irradiance
              is required. Its a float. Unit is degrees.
        lamda - Longitude of the location at the Moon where solar
                irradiance is required. Its a float. Unit is degrees.
        alpha - Angle between surface and the horizon. Its a float.
                Unit is degrees.
        beta - surface azimuth angle. Its a float. Unit is degrees.
    Return:
        Q - Solar Irradiance value. Its a float. Unit is W/m^2
    """
    So = 1361. # W/m**2
    Ro = 1. #au
    lamda = np.radians(lamda)
    phi = np.radians(phi)
    tau = np.radians(solar_azimuth)
    theta = np.radians(90 - elevation)
    # ra = np.radians(lon)
    # dec = np.radians(lat)
    # h = ra - lamda
    #cos_theta = np.sin(phi)*np.sin(dec)+np.cos(phi)*np.cos(dec)*np.cos(h)
    #theta = np.arccos(cos_theta)
    omega = tau - np.radians(beta)
    Q = So*(Ro/Rm)**2*(np.cos(alpha)*np.cos(theta)+\
        np.sin(alpha)*np.sin(theta)*np.cos(omega))*(np.cos(theta)>0)
    return Q

def get_insolation_ephemeris(
    start_time,
    end_time,
    step_size,
    phi,
    lamda,
    alpha=0.,
    beta=0.,
):
    """
    Get the ephemeris data as a pandas framework. The ephemeris is
    downloaded using the API provided by JPL Horizon.
    More info at: https://ssd.jpl.nasa.gov/horizons/

    Arguments:
        start_time: A string containing the start time in the format
                    supported by JPL Horizon.
        end_time: A string containing the end time in the format
                  supported by JPL Horizon.
        step_size: A string containing the step size of time in
                   the format supported by JPL Horizon.
        phi - Latitude of the location at the Moon where solar irradiance
              is required. Its a float. Unit is degrees.
        lamda - Longitude of the location at the Moon where solar
                irradiance is required. Its a float. Unit is degrees.
        alpha - Angle between surface and the horizon. Its a float.
                Unit is degrees.
        beta - surface azimuth angle. Its a float. Unit is degrees.
        
    Return:
        df: A pandas dataframe with following columns:
        Q -- solar irradiance (W/m^2)
        Distance -- Distance between Sun and Moon at the given time in AU.
                    Its a float.
        Solar azimuth -- solar azimuth angle in degrees. 
            North(0) -> East(90) -> South(180) -> West(270) -> North (360)
        Solar elevation -- elevation angle of sun in degrees. (-90 to +90) 
        phi -- Latitude of the location at the Moon where solar irradiance
              is required. Its a float. Unit is degrees.
        lamda -- Longitude of the location at the Moon where solar
                irradiance is required. Its a float. Unit is degrees.
        alpha -- Angle between surface and the horizon. Its a float.
                Unit is degrees.
        beta -- surface azimuth angle. Its a float. Unit is degrees.

    """

    # Obtaining the Moon-Sun distance ephemeris
    rm_data = get_data_from_jplh(
            start_time,
            end_time,
            step_size,
            quantities='19', # code for Moon-Sun distance and its rate
            target='301', # Moon
            observe_body='10' # Sun
    )
    # Obtaining the solar azimuth and elevation(90-zenith angle)
    azi_elev_data = get_data_from_jplh(
            start_time,
            end_time,
            step_size,
            quantities='4', # code for solar azimuth angle and elevation
            target='10', # Sun
            observe_body='301', # Moon
            phi=phi,
            lamda=lamda,
    )
    
    df = pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Distance",
            "Solar Azimuth",
            "Solar Elevation",
        ]
    )
    assert len(rm_data)==len(azi_elev_data)
    for i in range(1, len(rm_data) - 1):
        rm_data[i] = rm_data[i].split()
        azi_elev_data[i] = azi_elev_data[i].split()
        df.loc[len(df)] = rm_data[i][:-1]+azi_elev_data[i][-2:]

    to_float(
        df, ["Distance","Solar Azimuth","Solar Elevation"]
    )

    df["Q"] = get_solar_irradiance(
        Rm=df["Distance"],
        solar_azimuth=df["Solar Azimuth"],
        elevation=df["Solar Elevation"],
        phi=phi,
        lamda=lamda,
        alpha=alpha,
        beta=beta,
    )
    return df
