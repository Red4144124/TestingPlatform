#!/bin/bash

# Copyright 2023 RnD Center "ELVEES", JSC

sync; dd if=/dev/zero of=tempfile bs=1M count=1024; sync
sudo /sbin/sysctl -w vm.drop_caches=3
dd if=tempfile of=/dev/null bs=1M count=1024
