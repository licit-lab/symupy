"""
Abstract Observer 
=================
This module implements a general metaclass of the observer.
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import abc

# ============================================================================
#  CLASS AND DEFINITIONS
# ============================================================================


class AbsObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, value):
        """Local update method to retrieve subject data"""
        pass

    def __enter__(self):
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass
