""" 
No Command 
==========
"""
# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.abstractions import AbsCommand

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class NoCommand(AbsCommand):
    names = ("NoCommand",)
    description = "This is a no command"

    def execute(self):
        pass
