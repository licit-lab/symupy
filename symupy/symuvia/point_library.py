"""
    Symuvia Library Depender Analyzer:

    This script has objective to read library dependencies in Symuvia and 
    update those dependencies with respect to the folder where the script is placed. 

    Verify that the following placement is within the library .

    Symuvia 
      |_ sym_lib_dpa.py
      |_ Contents
          |_ Frameworks 
              |_ *.dylib     

    Usage: 
    
    Change into directory Symuvia (See figure above)

    Run: 

    python3 sym_lib_dpa.py 
        Runs the verification of dependencies for all libraries 

    python3 sym_lib_dpa.py mod
        Modyfies dependencies for all existing libraries within Contents/Frameworks 

    python3 sym_lib_dpa chk libname
        Check dependencies of a single library 
        ex.  
            python3 sym_lib_dpa chk libSymuVia.dylib

    python3 sym_lib_dpa mod libname
        Modyfies dependencies of a single library libname within Contents/Frameworks 
        ex.  
            python3 sym_lib_dpa mod libSymuVia.dylib

    Requirements: Python 3.6 or later
"""

__author__ = "Andres Ladino"
__copyright__ = "SymuPy Project"
__credits__ = ["Cecile Becarie"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Andres Ladino"
__email__ = "andres.ladino@ifsttar.fr"
__status__ = "Prototype"

import os 
import subprocess 
import re
import sys 

print(f'Script launched from: {os.getcwd()}')
libFolder = ('Contents','Frameworks')
libFiles = os.listdir(os.path.join(os.getcwd(), *libFolder))
libFilesFlt = [fileName for fileName in libFiles if fileName.split('.')[-1]=='dylib']

def modify_dependency(start_dir, end_dir, library):
    """
        Modify the dependencies from star_dir to end_dir for a library 
        star_dir: absolute path of the dependency 
        end_dir: new absolute path to the dependency
        library: name library 

        The function launches 

        install_name_tool -change star_dir end_dir library 
    """
    action = '/usr/bin/install_name_tool'
    option = '-change'
    sub_call = [action, option, start_dir, end_dir, library]
    subprocess.Popen(sub_call)
    return sub_call 

def call_dependency(libFullName):
    """
        Determine all dependencies for a single library in the 
        full absolute path 
    """
    action = '/usr/bin/otool'
    option = '-L'
    sub_call = [action, option, libFullName]
    return subprocess.Popen(sub_call , stdout=subprocess.PIPE)

def find_pattern(text_to_search):
    """
        Find pattern .dylib within a text 
    """
    pattern = re.compile(r'[a-zA-Z0-9_.+-]+\.dylib')
    matches = pattern.findall(text_to_search)

    pattern_path = re.compile(r'[a-zA-Z0-9_.+-/@]+\.dylib')  
    matches_path = pattern_path.findall(text_to_search)      

    irregular_patterns = [r'\/Python',
                          r'\/CoreFoundation',
                          r'\/CoreServices',
                         ]  
    irregular_dir_patterns = [r'[a-zA-Z0-9_.+-/]+/Python',
                              r'[a-zA-Z0-9_.+-/]+/CoreFoundation',                              
                              r'[a-zA-Z0-9_.+-/]+/CoreServices',
                              ]

    list_irregular_matches = []
    list_irregular_path_matches = []

    for irr_pattern, irr_dir_pattern in zip(irregular_patterns,irregular_dir_patterns):
        
        pattern_irr = re.compile(irr_pattern)
        pattern_path_irr = re.compile(irr_dir_pattern)

        matches_irr = pattern_irr.findall(text_to_search) 
        matches_path_irr = pattern_path_irr.findall(text_to_search)

        list_irregular_matches  = list_irregular_matches + matches_irr
        list_irregular_path_matches = list_irregular_path_matches + matches_path_irr


    matches_def = matches + list_irregular_matches
    matches_def_path = matches_path + list_irregular_path_matches

    return (matches_def[0], matches_def_path[0])

def update_dependencies(libFullName):
    """
        Update the library dependencies for libraries that are detected 
        within the folder 
    """
    bPrint = True
    oDependency = call_dependency(libFullName)
    sLibrary = libFullName.split('/')[-1]
    print(f'\n\t\t\tModifying dependencies for: {sLibrary}'.upper())
    iterDepend = iter(oDependency.stdout)
    next(iterDepend)
    for dep in iterDepend:
        full_query = dep.decode('utf-8')        
        lib_name, old_path = find_pattern(full_query)
        full_path = os.path.join(curr_path, *libFolder)
        new_path = os.path.join(full_path, lib_name) 
        if bPrint:
            print(f'\nOutput query:\n{full_query}')
            print(f'\t-Library name:\t{sLibrary}\n\t-Current path:\t{old_path}\n\t-Modifyd path:\t{new_path}')
        if os.path.isfile(new_path):
            print(f'\t\tUpdating dependency for {sLibrary} with {lib_name}')
            modify_dependency(old_path, new_path, libFullName)

def verify_dependencies(libFullName):
    """
        Verify library dependencies, printout of the current dependencies 
    """
    bPrint = True    
    oDependency = call_dependency(libFullName)
    sLibrary = libFullName.split('/')[-1]    
    print(f'\n\n\t\t\tListing dependencies for: {sLibrary}'.upper())
    iterDepend = iter(oDependency.stdout)
    next(iterDepend)
    for dep in iterDepend:
        full_query = dep.decode('utf-8') 
        lib_name, old_path = find_pattern(full_query)        
        full_path = os.path.join(curr_path, *libFolder)
        new_path = os.path.join(full_path, lib_name)        
        if bPrint:            
            print(f'\nOutput query:\n{full_query}')
            print(f'\t-Library reference:\t{sLibrary}\n\t-Current path:\t{old_path}') 
        if os.path.isfile(new_path):
            if new_path==old_path:
                print('Library dependencies have been updated')          

if __name__ == '__main__':
    curr_path = os.getcwd()
    full_path = os.path.join(curr_path, *libFolder)
    print(f'Current path: {curr_path}')
    j = 0
    n = 100 

    # Check 2nd argument for a specific library 
    if len(sys.argv)==3:
        libFilesFlt = [sys.argv[2]]

    for file_name in libFilesFlt:
        if j<n:
            full_file_name = os.path.join(full_path, file_name)    
            print(f'Analyzing: {full_file_name}')
            if len(sys.argv) >= 2:                         
                if sys.argv[1]=='mod':
                    update_dependencies(full_file_name)
                    verify_dependencies(full_file_name)
                else: 
                    verify_dependencies(full_file_name) 
            else:
                verify_dependencies(full_file_name) 
        else: 
            print(f'Max number of {n} libraries updates reached.')
            break
        j+=1

