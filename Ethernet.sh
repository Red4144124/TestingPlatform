#!/bin/bash

interface_names=($(ip -o link show | awk -F': ' '{print $2}'))

for interface in "${interface_names[@]}"; do
    echo "Тестирование интерфейса $interface"
    ethtool -t "$interface"
    echo "------------------------------"
done