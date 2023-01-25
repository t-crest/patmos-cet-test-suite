import os
import subprocess
import sys
from shutil import which
import re
import random

if which("patmos-clang") is None:
    print("Patmos simulator 'patmos-clang' could not be found.")
    sys.exit(1)

if which("pasim") is None:
    print("Patmos simulator 'pasim' could not be found.")
    sys.exit(1)
    
# Parse arguments

# The source file to test
source_to_test = ""

sources_end = 1
while(sys.argv[sources_end] != "__END_SOURCES__"):
    source_to_test = source_to_test + " " + sys.argv[sources_end]
    sources_end += 1

# The compiled file
compiled = sys.argv[sources_end+1]   

# Which function is the root single-path function
sp_root = sys.argv[sources_end+2]


if len(sys.argv) > sources_end+3:
    if sys.argv[sources_end+3]=="false":
        check_all = False
    elif sys.argv[sources_end+3]=="true":
        check_all = True
    else:
        print("Invalid 'check_all' argument. Should be 'true' or 'false' but was'", sys.argv[sources_end+3], "'")
        sys.exit(1)
else:
    check_all = True


# Test result
exit_code=0
found_error=False

def throw_error(args, *msgs):
        global found_error
        for msg in msgs:
            print(msg, end = '')
        print("\nCompiler args:", args, "\n\n")
        found_error=True

def run_and_time(seed, must_exec_correct, args):
        out = subprocess.run(["pasim", compiled, "-V"],stderr=subprocess.PIPE,input=str(seed), encoding='ascii')
        if must_exec_correct and out.returncode != 0:
            throw_error(args, "Execution failed for '", compiled, "' using seed ", seed)
            return
        
        sp_root_cycles_regex = "<" + sp_root + ">\n.*\n\s*1\s*(\d*)"
        matches = re.search(sp_root_cycles_regex, out.stderr)
        
        if matches == None:
            throw_error(args, "Couldn't find cycle count.")
            return 0
        else:
            return int(matches.group(1))

# Compile and test using the given compiler arguments.
# if 'ensure_all' is true, checks that running the program with any seed executes successfully.
# if false, only checks when given the seed 0
def compile_and_test(args, ensure_all):
    global exit_code
    global found_error
    found_error = False
                        
    compiler_args = source_to_test + " " + os.path.dirname(__file__) + "/lib/rand.c -o " + compiled + " -O2 -mpatmos-enable-cet -mpatmos-cet-functions=" + sp_root + " " + args + " -I" + os.path.dirname(__file__) + "/include"
             
    # Compile
    if subprocess.run(["patmos-clang"] + compiler_args.split()).returncode != 0:
        throw_error(args, "Failed to compile '", source_to_test, "'")
        exit_code=123
        return
    
    # Run with seed 0
    cycles = run_and_time(0, True, args)
    if found_error:
        exit_code=123
        return
    
    for i in range(0,10):
        seed = random.randint(1, 2147483647) #32-bit int
        next_cycles = run_and_time(seed, ensure_all, args)
        
        if found_error:
            exit_code=123
            return
        
        if next_cycles != cycles:
            throw_error(args, "Unequal execution time seed '", seed, "'") 
            exit_code=123
            return

compile_and_test("-mllvm --mpatmos-enable-cet=opposite", check_all)
compile_and_test("-mllvm --mpatmos-enable-cet=counter", check_all)
compile_and_test("", check_all)
compile_and_test("-mllvm --mpatmos-enable-cet=opposite -mllvm --mpatmos-disable-pseudo-roots", check_all)
compile_and_test("-mllvm --mpatmos-enable-cet=counter -mllvm --mpatmos-disable-pseudo-roots", check_all)
compile_and_test("-mllvm --mpatmos-disable-pseudo-roots", check_all)
compile_and_test("-mllvm --mpatmos-enable-cet=opposite -mllvm --mpatmos-disable-vliw=false", check_all)
compile_and_test("-mllvm --mpatmos-enable-cet=counter -mllvm --mpatmos-disable-vliw=false", check_all)
compile_and_test("-mllvm --mpatmos-disable-vliw=false", check_all)

# Success?
sys.exit(exit_code)
