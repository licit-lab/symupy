"""
Main Command Line Interface
===========================
This file groups all the commands contained in the cli menu for symupy
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import sys
import click

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.screen import log_verify
from symupy.postprocess.visunet.main import launch_app

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

help_text = """Symupy

A package to launch traffic simulations using SymuFlow

This is a Command Line Interface to provide functionalities related to specific task executions and

Please visit: symupy.readthedocs.io/ for more information.
"""

# ------------------------------ Main command----------------------------------


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Increase verbosity.")
def main(verbose: bool) -> int:
    """SymuFlow main CLI launcher"""
    if verbose:
        log_verify(help_text)
    return 0


# ------------------------------ Launch command--------------------------------


@main.command()
@click.option(
    "-s",
    "--scenario",
    default="",
    multiple=False,
    help="Scenario file(s) under analysis.",
)
def launch(scenario: str) -> None:
    """Launches a simulation """
    pass


# ------------------------------ Visunet command--------------------------------


@main.command()
@click.option(
    "-f",
    "--file",
    default=None,
    help="SymuFlow network.",
)
def visu(file) -> None:
    """Launches VisuNet app """
    launch_app(file)


# ------------------------------ Analyze command-------------------------------


@main.command()
@click.option(
    "-f",
    "--file",
    default="",
    multiple=False,
    help="Scenario file(s) under analysis.",
)
def analyze(scenario: str) -> None:
    """Analyzes a specific output file """
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
