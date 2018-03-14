## Why this strategy failed!

- As can be checked in the source files, the [`should drop
  privileges`](https://android.googlesource.com/platform/system/core/+/android-cts-8.1_r3/adb/daemon/main.cpp#62)
  always returns `1` when the compiler flag `ALLOW_ADBD_ROOT` is not set. This 
  flag is only set for [`userdebug` and `eng`
  builds](https://android.googlesource.com/platform/system/core/+/android-cts-8.1_r3/adb/Android.mk#355).

- Due to compile time optimisations, the [code to keep the root previleges never
  lands in the compiled
  binary](https://android.googlesource.com/platform/system/core/+/android-cts-8.1_r3/adb/daemon/main.cpp#129).

  ```objdump
    0x00404ea4      af780194       bl sym.minijail_new         ;[4]                                                                                                                       
    0x00404ea8      680800d0       adrp x8, 0x512000 ; "d    allocated      nmalloc      ndalloc    nrequests 
    0x00404eac      08b11891       add x8, x8, 0x62c                                                                                                                                      
    0x00404eb0      61018052       movz w1, 0xb                                                                                                                                           
    0x00404eb4      e2430191       add x2, sp, 0x50                                                                                                                                       
    0x00404eb8      00c1c13c       ldur q0, [x8, 0x1c]         ; section_end..note.gnu.gold_version ; [0x1c:4]=-1                                                                         
    0x00404ebc      f30300aa       mov x19, x0                                                                                                                                            
    0x00404ec0      020540ad       ldp q2, q1, [x8]                                                                                                                                       
    0x00404ec4      e0c3863c       stur q0, [sp + local_6ch]                                                                                                                              
    0x00404ec8      e28702ad       stp q2, q1, [sp + local_50h]                                                                                                                           
    0x00404ecc      c6780194       bl sym.minijail_set_supplementary_gids ;[5] NO CONDITIONAL JUMP AFTER THIS                                                                                                        
    0x00404ed0      e1071a32       orr w1, wzr, 0xc0                                                                                                                                      
    0x00404ed4      e00313aa       mov x0, x19                                                                                                                                            
    0x00404ed8      fd780194       bl sym.minijail_capbset_drop ;[6]                                                                                                                      
    0x00404edc      14fa8052       movz w20, 0x7d0                                                                                                                                        
    0x00404ee0      e00313aa       mov x0, x19                                                                                                                                            
    0x00404ee4      e103142a       mov w1, w20                                                                                                                                            
    0x00404ee8      b0780194       bl sym.minijail_change_gid  ;[7]                                                                                                                       
    0x00404eec      e00313aa       mov x0, x19                                                                                                                                            
    0x00404ef0      e103142a       mov w1, w20                                                                                                                                            
    0x00404ef4      9e780194       bl sym.minijail_change_uid  ;[8]                                                                                                                       
    0x00404ef8      e00313aa       mov x0, x19                                                                                                                                            
    0x00404efc      04790194       bl sym.minijail_enter       ;[9]
  ```
- So, an important function, [`selinux_android_setcon`](https://android.googlesource.com/platform/system/core/+/android-cts-8.1_r3/adb/daemon/main.cpp#132)
  never enters the binary. As
  this is a static binary, we can't patch the import tables to link in the
  function as well (although I am not sure we can do that, but I believe we
  can).

- Since the checking of the flag landed in a very [early version of
  android](https://android.googlesource.com/platform/system/core/+/5890fe33141a9efd124c86c40a8c1ff6170ecf20%5E!/)
  I don't think we can do much about it either, except for compiling our own
  version!

- As some of the selinux functions like `selinux_android_restorecon` were
  present, I thought that we can recreate the `selinux_android_setcon` function in the binary. But I was
  not able to find the source code of `setcon`.

Considering the above point, I came to the conclusion that this trick to gain
adbd root won't work on any device. The best we can do is to use an adbd binary
from an `userdebug` compiled platform.
