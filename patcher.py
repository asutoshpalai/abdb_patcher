#!/usr/bin/env python2
"""
Script to patch adbd binary by ro.debuggable check and privilege dropping
"""

import sys
import json
import shutil
import r2pipe

if len(sys.argv) != 3:
    print("Usage : %s <input> <patched_output>" % sys.argv[0])
    sys.exit(1)

input = sys.argv[1]
output = sys.argv[2]

shutil.copy2(input, output)

r2 = r2pipe.open(output, ['-w'])
print(r2.cmd('aa'))
print(r2.cmd('s sym.__android_log_is_debuggable'))
print(r2.cmd('"wa mov x0, 1; ret"'))
nop_address = [json.loads(r2.cmd("axtj sym.minijail_capbset_drop"))[0]['from'],
                json.loads(r2.cmd("axtj sym.minijail_change_gid"))[0]['from'],
                json.loads(r2.cmd("axtj sym.minijail_change_uid"))[0]['from']]

for addr in nop_address:
    r2.cmd('wa nop @ %d' % addr)
r2.quit()
