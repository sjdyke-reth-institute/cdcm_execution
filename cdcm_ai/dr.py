#~ovn!
"""Meta-programs for generating AI that does diagnostic reasoning

Author:
    R Murali Krishnan
    
Date:
    04.10.2023
    
"""


import numpy as np
import networkx as nx

from cdcm import *
from cdcm_abstractions import *

from typing import List, Set
from functools import cached_property
from pprint import pprint

TestResult = bidict({"PASS": 0, "FAIL": 1, "UNKNOWN": -1})

FailureModeClass = bidict({"GOOD": 1, "SUSPECT": 2, "BAD": 3, "UNKNOWN": -1})



class DiagnosticReasoner:
    """System that performs diagnostic reasoning"""
    
    @property
    def system(self) -> System:
        """Getter method for the system"""
        return self._system
    
    @system.setter
    def system(self, val: System):
        """Setter method for the system"""
        assert isinstance(val, System)
        self._system = val

    @cached_property
    def health_status_vars(self) -> Set[HealthStatus]:
        """Getter method for health status variables"""
        return self.system.get_nodes_of_type(HealthStatus)
    
    @cached_property
    def test_vars(self) -> Set[Test]:
        """Getter method for test variables"""
        return self.system.get_nodes_of_type(Test)
    
    @cached_property
    def nhs(self):
        """Getter function for the number of health status variables"""
        return len(self.health_status_vars)
    
    @cached_property
    def ntests(self):
        """Getter function for the number of test variables"""
        return len(self.test_vars)
    
    @cached_property
    def dmatrix(self):
        """Getter function for the D-matrix of the reasoner"""
        _dmatrix = np.zeros((self.nhs, self.ntests))

        for j, test in enumerate(self.test_vars):
            for i, hs in enumerate(self.health_status_vars):
                path_exists = nx.has_path(self.system.dag, hs, test)
                _dmatrix[i,j] = int(path_exists)
        return _dmatrix

    def __init__(self, system: System, **kwargs):
        self.system = system

    def run(self):
        """Run the diagnostic reasoning algorithm"""

        test_results = [t.value for t in self.test_vars]
        failure_class = [FailureModeClass["UNKNOWN"] for _ in range(self.nhs)]

        # Classify failure-modes as either `GOOD`, `SUSPECT` or `UNKNOWN` (default)
        for tid, test_result in enumerate(test_results):
            for hsid in range(self.nhs):
                if self.dmatrix[hsid, tid] == 1:
                    # There exists a directed path from
                    # the failure-mode `HealthStatus` variable
                    # to the `Test` variable
                    if test_result == TestResult["PASS"]:
                        failure_class[hsid] = FailureModeClass["GOOD"]
                    elif test_result == TestResult["FAIL"]:
                        if failure_class[hsid] != FailureModeClass["GOOD"]:
                            failure_class[hsid] = FailureModeClass["SUSPECT"]
        
        # Check if the `SUSPECT` failure modes are actually `BAD`
        test_implies_failure = lambda h, t: (self.dmatrix[h,t] == 1) and \
            (test_results[t] == TestResult["FAIL"])
        for hsid in range(self.nhs):
            if failure_class[hsid] == FailureModeClass["SUSPECT"]:
                # Check `SUSPECT` variables for `BAD`
                for tid in range(self.ntests):
                    if test_implies_failure(hsid, tid):
                        count_implicated = 0
                        for _hsid in range(self.nhs):
                            if (self.dmatrix[_hsid, tid] == 1) \
                            and (failure_class[_hsid] in \
                                 [FailureModeClass["SUSPECT"], FailureModeClass["BAD"]]):
                                count_implicated += 1                                
                        if count_implicated == 1:
                            failure_class[hsid] = FailureModeClass["BAD"]
                        else:
                            # All other cases, the failure mode is `SUSPECT`
                            pass
        dict_failure_class = {hs.absname: (fail_class, hs) for hs, fail_class in zip(self.health_status_vars, failure_class)}
        return dict_failure_class
    
    def process(self, verbose: bool=False) -> HealthStatus:
        """Perform health management"""

        dr_results = self.run()

        bad_health_states = [k for n, (val, k) in dr_results.items() if val == FailureModeClass["BAD"]]

        if bad_health_states:
            if verbose:
                print(f"---@time={self.system.clock.t.value}hr :: ",
                    [hs.absname + ": " + str(hs.value) for hs in bad_health_states], 
                    " are the identified bad health states")
            return bad_health_states[0]
        else:
            return []
        
    def __repr__(self) -> str:
        return f"DiagnosticReasoner(sys={repr(self.system)}, size=[{self.nhs}x{self.ntests}])"

    
