"""Some utility functions that do not fit anywhere else.

Author:
    Ilias Bilionis

Date:
    3/13/2022

"""


__all__ = ["TEXT_TRIMMING_SIZE", "trim_str"]


# Default text rimming size
# TODO: Make the parameter adjustable from configuration file.
TEXT_TRIMMING_SIZE = 20


def trim_str(text, size=TEXT_TRIMMING_SIZE):
    """
    Returns a trimmed version of the `text`.

    If the `text` is smaller than `size`,
    then it returns `text`.
    Otherwise, it returns `text[:size]`.
    """
    if len(text) < size:
        return text
    else:
        return text[:size] + " ..."
