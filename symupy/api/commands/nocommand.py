""" 
No command 
====================================
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.metaclass.command import AbsCommand

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class NoCommand(AbsCommand):
    names = ("NoCommand",)
    description = "This is a no command"

    def execute(self):
        pass
        # click.echo(click.style("No command is executed", fg="blue", bold=True))
