"""
CSV Parser
==========
A module to parse information from SymuFlow output CSVs
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import re
from collections import defaultdict, OrderedDict


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


def get_iteration_PPaths(file):
    file = open(file)
    nb_iter = defaultdict(OrderedDict)
    start = 0
    prev_line = None
    for count, line in enumerate(file):
        if "Total travel time on the assignment period is" in line:
            # nb_iter.append([start, count-3])
            col = prev_line.split(";")
            nb_iter[int(col[0])][int(col[1])] = [start, count - 1]
            start = count + 3
        prev_line = line

    return dict(nb_iter)


def get_iteration_final_PPaths(file):
    file = open(file)
    nb_iter = OrderedDict()
    start = 0
    prev_line = None
    for count, line in enumerate(file):
        if "Total travel time on the assignment period is" in line:
            # nb_iter.append([start, count-3])
            col = prev_line.split(";")
            nb_iter[int(col[0])] = [start, count - 1]
            start = count + 3
        prev_line = line

    return dict(nb_iter)


def get_iteration_distribution(file):
    file = open(file)
    nb_iter = defaultdict(lambda: defaultdict(OrderedDict))
    start = 1
    prev_line = ""
    prev_prev_line = None
    inner_loop = 0
    outer_loop = 0
    for count, line in enumerate(file):
        # if line.strip() == '' and prev_line.strip() == '':
        if (line + prev_line).strip() == "":
            period = int(prev_prev_line.split(";")[0])
            outer_loop = int(prev_prev_line.split(";")[1])
            inner_loop = int(prev_prev_line.split(";")[2])
            nb_iter[period][outer_loop][inner_loop] = [start, count - 2]
            start = count + 1
        prev_prev_line = prev_line
        prev_line = line

    return {key: dict(val) for key, val in nb_iter.items()}
