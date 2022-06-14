# Patmos Constant Execution Time Test Suite

This test suite is meant to test the generation of constant execution time code.
It contains whole programs that are compiled and run with random inputs.
The tests then check that the execution produces the correct result and that all runs execute in the same number of cycles (for the functions designated as constant execution time).

# Requirements

Assumes the patmos compiler `patmos-clang` is available on the `PATH` and that `llvm-lit` is also available (through not necessarily on the path).

# Running the tests

Running the tests is quite simple. From the root directory run the command:

```
llvm-lit . -v
```

Here `llvm-lit` should be a valid path to the [LLVM `lit` tool](https://llvm.org/docs/CommandGuide/lit.html).
If you have a build of the `patmos-llvm-project` repository, the tool should be found under `patmos-llvm-project/build/bin/llvm-lit`.

The test runs using the isntalled `patmos-clang`. So if you are testing a local build, remember to update the installation after each build of LLVM.