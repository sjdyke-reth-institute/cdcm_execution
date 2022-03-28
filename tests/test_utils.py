"""Test the common utilities

Author:
    Murali Krishnan R

Date:
    3/18/2022
"""

import numpy as np
import pytest
from cdcm import clip


class TestClip:

    def test_clip_utility_inputs(self):
        """Tests for the inputs for the clipping utility"""
        # 1. Incorrect value
        with pytest.raises(Exception):
            clip("str")
        # 2. Both edges cannot be `None`
        min_value, max_value = None, None
        value = np.linspace(0, 1, 11)
        with pytest.raises(Exception):
            clip(value, min_value, max_value)

    def test_clip_utility_scalars(self):
        """Test the functionality of the clip utility"""
        min_value, max_value = 0.3, 0.7
        value = 0.8
        assert clip(value, max_value=max_value) == max_value

        value = 0.2
        assert clip(value, min_value=min_value) == min_value

        value = np.linspace(0, 1, 21)
        assert np.array_equal(clip(value, min_value, max_value), \
                              np.clip(value, min_value, max_value))


