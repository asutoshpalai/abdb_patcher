#!/usr/bin/env python2
"""
Script to patch adbd binary by ro.debuggable check

We could have modified the binary through r2 but there is a bug due to which
r2 makes unnessary writes. Refer to the following GitHub issue for details:
    https://github.com/radare/radare2/issues/9489

As a hack, we are reading about 40 bytes, making there required changes through
hardcoded asm codes and using string find and replace over the binary.
"""

import sys
import r2pipe

if len(sys.argv) != 3:
    print("Usage : %s <input> <patched_output>" % sys.argv[0])
    sys.exit(1)

input = sys.argv[1]
output = sys.argv[2]

import r2pipe
r2 = r2pipe.open(input)
r2.cmd('af')
orig = r2.cmd('p8 40 @ sym.__android_log_is_debuggable').decode('hex')
new = '200080d2'.decode('hex') + 'c0035fd6'.decode('hex') + orig[8:]
r2.quit()

with open(input, 'r') as f:
    bin = f.read()

bin = bin.replace(orig, new)

with open(output, 'wb') as f:
    f.write(bin)
