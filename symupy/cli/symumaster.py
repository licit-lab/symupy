"""
Symumaster Module
=================
    We provide here assets to launch the simulations via symuaster.
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
from pathlib import Path
import subprocess, time, os, sys

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.screen import log_error, log_in_terminal, log_verify
from symupy.utils.exceptions import SymupyError, SymupyFileLoadError


class SymuMasterHandler:
    """SymuMaster Handler class stores information of an scenario."""

    def __init__(self, cfgfile: str = ""):
        if Path(cfgfile).exists():
            log_verify(f"\tConfig file: {cfgfile}")
            self.cfgfile = cfgfile
        else:
            raise SymupyFileLoadError("\tThe provided path could not be found")

    def run_subprocess(self):
        cmd = ["SymuMasterLauncher", "-I", self.cfgfile]
        # cmd = ["ls", "-alh"]
        try:
            p = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            for line in iter(p.stdout.readline, b""):
                log_in_terminal(
                    "\t " + line.rstrip().decode("UTF-8"), fg="bright_black"
                )
        except FileNotFoundError:
            raise SymupyError("\tSymuMaster N/A. Please install", " ".join(cmd))


if __name__ == "__main__":
    path = os.path.join(
        os.getcwd(), "tests/mocks/bottlenecks/bottleneck_001.xml"
    )
    sh = SymuMasterHandler(path)
    sh.run_subprocess()
