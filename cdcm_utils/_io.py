"""Input/Output utilities

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


import yaml
import numpy.typing as npt
from typing import Dict, Any
from cdcm import SimulationSaver


def parse_yaml(filepath: str, **kwargs) -> Dict[str, Dict[str, Any]]:
    """Parse a `.yaml` file and return content as a dict of dicts"""
    with open(filepath, "r") as f:
        filecontents = yaml.safe_load_all(f)
        parsed_content = [content for content in filecontents]
    return parsed_content[0] if len(parsed_content) == 1 else parsed_content



def extract_data_from_saver(
    saver: SimulationSaver, 
    namedfilehandles: Dict[str, str]
    ) -> Dict[str, npt.NDArray]:
    """Utility to extract data from a `cdcm.SimulationSaver` instance
    
    Arguments
    ---------
    saver               :   cdcm.SimulationSaver
        A simulation saver object
    namedfilehandles    :   Dict[str, str]
        Map of shorthand to data to their `filehandles` as in the saver object

    Returns
    -------
        Dict[str, npt.ndarray]
        Map of data (np.ndarray) to shorthand handles passed to this utility
    """

    named_data = dict()
    for name, filehandle in namedfilehandles.items():
        try:
            named_data[name] = saver.file_handler[filehandle][:]
        except:
            msg = f"<< {filehandle} >> not found in saver object"
            raise RuntimeError(msg)
    return named_data