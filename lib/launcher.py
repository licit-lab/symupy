import os
import subprocess
import sys

lib_rel_path = ('darwin',)
lib_file_names = os.listdir(os.path.join(os.getcwd(), *lib_rel_path))
lib_file_names_flt = [fi for fi in lib_file_names if fi.endswith(".dylib")]

if __name__ == "__main__":

    arg_var = tuple(sys.argv)

    try:
        mode = arg_var[1] if len(arg_var) > 1 else "ck"
        lib_rel_path, lib_name = os.path.split(arg_var[2])
        lib_rel_path = (lib_rel_path,)
        lib_file_names_flt = [lib_name]
    except IndexError:
        print(" ")

    for fi in lib_file_names_flt:
        fi_path = os.path.join(*lib_rel_path, fi)
        fi_n = fi.split('.')[0]
        subprocess.run(f"mkdir log/{fi_n}", shell=True)
        subprocess.run(
            f"python3 spydsla.py md {fi_path} > log/{fi_n}/darwin__$(date +%Y-%m-%d_%H:%M:%S)_md.log", shell=True)
        subprocess.run(
            f"python3 spydsla.py ck {fi_path} > log/{fi_n}/darwin__$(date +%Y-%m-%d_%H:%M:%S)_ck.log", shell=True)
