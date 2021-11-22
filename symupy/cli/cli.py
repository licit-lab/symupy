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
from click.core import Context

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.screen import log_verify, log_warning
from symupy.cli.symumaster import SymuMasterHandler

try:
    from symupy.postprocess.visunet.main import launch_app
except ImportError:
    log_warning("Non physical terminal, monitor interface not available")


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
    """SymuPy main command line launcher"""

    if verbose:
        log_verify(help_text)

    return 0


# ------------------------------ Launch command--------------------------------


@main.command()
@click.option("-m", "--symumaster", is_flag=True, help="Runs with symumaster")
@click.argument("SCENARIO", type=str)
def run(scenario: str, symumaster: bool) -> None:
    """Launches a simulation"""
    if symumaster:
        SymuMasterHandler(scenario).run_subprocess()


# ------------------------------ Visunet command--------------------------------


@main.command()
@click.option(
    "-f",
    "--file",
    default=None,
    help="SymuFlow network.",
)
def visualize(file) -> None:
    """Launches VisuNet app"""
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
    """Analyzes a specific output file"""
    pass


if __name__ == "__main__":

    cmd = "-m /workspaces/symupy/tests/mocks/bottlenecks/bottleneck_002.xml"
    run(cmd.split())
    sys.exit(main())  # pragma: no cover
