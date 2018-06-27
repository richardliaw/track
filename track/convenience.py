"""
Miscellaneous helpers for extracting parameters, useful for creating
Trial param_maps without the hassle of extracting the parameters manually.
"""

import sys

def absl_flags():
    """
    Extracts absl-py flags that the user has specified and outputs their
    key-value mapping.
    """
    # TODO: need same thing for argparse
    from absl import flags
    flags_dict = flags.FLAGS.flags_by_module_dict()
    # only include parameters from modules the user probably cares about
    def _relevant_module(module_name):
        if __package__ and __package__ in module_name:
            return True
        if module_name == sys.argv[0]:
            return True
        return False
    return {
        flag.name: flag.value for module, flags in flags_dict.items()
        for flag in flags if _relevant_module(module)}
