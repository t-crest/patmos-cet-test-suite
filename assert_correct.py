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

# Compile and test using the given compiler arguments.
# if 'ensure_all' is true, checks that running the program with any seed executes successfully.
# if false, only checks when given the seed 0
def compile_and_test(args, ensure_all):
    def throw_error(*msgs):
        for msg in msgs:
            print(msg, end = '')
        print("\nCompiler args: ", args)
        sys.exit(1)
             
    def run_and_time(seed, must_exec_correct):
        out = subprocess.run(["pasim", compiled, "--print-stats", sp_root],stderr=subprocess.PIPE,input=str(seed), encoding='ascii')
        if must_exec_correct and out.returncode != 0:
            throw_error("Execution failed for '", compiled, "' using seed ", seed)
        
        cycles = re.findall('Cycles:\s*[0-9]+',out.stderr)
        
        if len(cycles) == 1: 
            return int(cycles[0].split(":")[1].strip())
        else:
            throw_error("Couldn't unambiguously find the cycles count using seed '", seed, "': ", out.stderr)
             
    compiler_args = source_to_test + " " + os.path.dirname(__file__) + "/lib/rand.c -o " + compiled + " -mpatmos-enable-cet -mpatmos-cet-functions=" + sp_root + " " + args + " -I" + os.path.dirname(__file__) + "/include"
             
    # Compile
    if subprocess.run(["patmos-clang"] + compiler_args.split()).returncode != 0:
        throw_error("Failed to compile '", source_to_test, "'")
    
    # Run with seed 0
    cycles = run_and_time(0, True)
    
    for i in range(0,10):
        seed = random.randint(1, 2147483647) #32-bit int
        next_cycles = run_and_time(seed, ensure_all)
        
        if next_cycles != cycles:
            throw_error("Unequal execution time seed '", seed, "'") 

compile_and_test("-O2", check_all)
compile_and_test("-O2 -mllvm --mpatmos-disable-pseudo-roots", check_all)
compile_and_test("-O2 -mllvm --mpatmos-enable-cet=opposite", check_all)
compile_and_test("-O2 -mllvm --mpatmos-enable-cet=counter", check_all)

# Success
sys.exit(0)
