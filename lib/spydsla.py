"""
    Symuvia Python Dynamic Shared Library Analyzer:

    This script has objective to read library dependencies in Symuvia and 
    update those dependencies with respect to the folder where the script is placed. 

    Run: 

    python3 spydsla.py 
        Runs the verification of dependencies for all libraries 

    python3 spydsla.py md
        Modyfies dependencies for all existing libraries within dirname:darwin 

    python3 spydsla ck dirname/libname
        Check dependencies of a single library 
        ex.  
            python3 spydsla ck darwin/libSymuVia.dylib

    python3 spydsla md dirname/libname
        Modyfies dependencies of a single library libname within dirname:darwin
        ex.  
            python3 spydsla md darwin/libSymuVia.dylib

    Requirements: Python 3.6 or later
    Compatibility: MacOS
"""

import typing
import sys
import re

import os
import subprocess

lib_rel_path = ("darwin",)
lib_file_names = os.listdir(os.path.join(os.getcwd(), *lib_rel_path))
lib_file_names_flt = [fi for fi in lib_file_names if fi.endswith(".dylib")]

dir_collect = []

pattern = re.compile(r"/?@?[a-zA-z0-9\./+-]+\.dylib")

excluded_paths = ["@rpath"]


def d2t(tag):
    return "exist" if tag else "absent"


def call_dependency(libFullName):
    """
        Determine all dependencies for a single library in the
        full absolute path
    """
    action = "/usr/bin/otool"
    option = "-L"
    sub_call = [action, option, libFullName]
    call_str = " ".join(sub_call)
    dep_enc = subprocess.check_output(call_str, shell=True)
    dep_lst = dep_enc.decode("UTF8").split("\n")
    return dep_lst[1:]


def modify_dependency(start_dir, end_dir, library):
    """
        Modify the dependencies from star_dir to end_dir for a library
        star_dir: absolute path of the dependency
        end_dir: new absolute path to the dependency
        library: name library

        The function launches

        install_name_tool -change star_dir end_dir library
    """
    action = "/usr/bin/install_name_tool"
    option = "-change"
    sub_call = [action, option, start_dir, end_dir, library]
    subprocess.Popen(sub_call)
    return sub_call


def verify_update_dependencies(lib_name, lib_rel_path, modify_dep=False):
    """
    Verify library dependencies, printout of the current dependencies
    """
    print(lib_name)
    global dir_collect
    try:
        target_dir = os.path.join(os.getcwd(), *lib_rel_path)
        lib_path = os.path.join(target_dir, lib_name)
        oDependency = call_dependency(lib_path)

        for dep in iter(oDependency.stdout):
            # print(dep)
            try:
                dsl_path = pattern.findall(dep.decode('utf-8'))[0]
            except IndexError:
                print(f"Undetected path in: {dep.decode('utf-8')}")
                continue
            dsl_filename = os.path.basename(dsl_path)
            dsl_dirname = os.path.dirname(dsl_path)
            dct_dep = {"lib": lib_name, "old_path": dsl_path, "exist_old": os.path.isfile(dsl_path)}
            print(f"  origin ({d2t(dct_dep['exist_old'])}): {dsl_path}")
            if dsl_dirname not in dir_collect:
                dir_collect.append(dsl_dirname)
            if (target_dir != dsl_dirname) and modify_dep:
                target_path = os.path.join(target_dir, dsl_filename)
                dct_dep["new_path"] = target_path
                dct_dep["exist_new"] = os.path.isfile(target_path)
                print(f"  target ({d2t(dct_dep['exist_new'])}): {target_path}")
                if (
                    dct_dep["exist_new"]
                    and not dct_dep["exist_old"]
                    and dsl_dirname not in excluded_paths
                ):
                    modify_dependency(dct_dep["old_path"], dct_dep["new_path"], lib_path)
                    print("\tDynamic Shared Library update: origin -> target")
    except StopIteration:
        raise FileNotFoundError(lib_path)


if __name__ == "__main__":
    curr_path = os.getcwd()
    full_path = os.path.join(curr_path, *lib_rel_path)

    arg_var = tuple(sys.argv)

    try:
        mode = arg_var[1] if len(arg_var) > 1 else "ck"
        lib_rel_path, lib_name = os.path.split(arg_var[2])
        lib_rel_path = (lib_rel_path,)
        lib_file_names_flt = [lib_name]
        print(
            "Verification for: {} in {}".format(
                lib_file_names_flt, os.path.join(os.getcwd(), *lib_rel_path)
            )
        )
    except IndexError:
        print("Verification for: All libraries")

    f_mode = True if mode == "md" else False

    # print(mode)
    # print(lib_file_names_flt)
    for lib_file in lib_file_names_flt:
        verify_update_dependencies(lib_file, lib_rel_path, f_mode)

    print(dir_collect)
