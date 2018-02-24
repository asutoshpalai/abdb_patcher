#!/usr/bin/env bash

setopt -e

echo "Grant root permission to adb(shell) in the prompt that will be displayed on the device"
adb shell "su -c 'cp /system/bin/adbd /data/local/tmp/adbd_orig'"
adb pull /data/local/tmp/adbd_orig ./remote_adbd
echo "Fetched adbd binary"

./patcher.py remote_adbd adbd_patched
adb push adbd_patched /data/local/tmp/adbd_patched

echo "Again grant root permission to adb(shell) in the prompt that will be displayed on the device"
adb shell "nohup su -c 'stop adbd && mount -o rw,remount /system && cp /data/local/tmp/adbd_patched /system/bin/adbd; start adbd' &>/dev/null"
