# ADB Daemon Patcher
Patches the adb daemon binary to allow `adb root` without setting the system
property `ro.debuggable`.

#### This works on rooted devices only

## Running

- Install [radare2](https://github.com/radare/radare2) and
  [r2pipe for
  python2](https://github.com/radare/radare2-r2pipe/tree/master/python).
- Clone the repo

      $ git clone https://github.com/asutoshpalai/adbd_patcher

- Run `adbd_patcher.sh`. Have the device screen unlocked, it will ask for root
  permission for adb shell.

      $ cd adbd_patcher && adbd_patcher.sh

- Root adbd

      $ adb root

_Note:_ This is not a permanent patch. The changes get reverted on reboot.

## Status

This was developed for Android 8.1 on LineageOS.

Although the patch is successful and the daemon restarts successfully, the `abd
root` failed for **me** as **my** ROM was not compiled with `ALLOW_ADBD_ROOT` flag. But
feel free to try for yourself. Nothing is permanent, everything reverts back
with the reboot. If it works, create an issue so that I can remove this message.
