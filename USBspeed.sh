#!/bin/bash

# Функция для логирования
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S"): $1" >> usb_log.txt
}

log "Скрипт запущен. Ожидание вставки флешки..."

# Ожидание подключения USB-устройства
while true; do
    udisksctl monitor | while read -r line; do
        if [[ $line == *"Added /org/freedesktop/UDisks2/block_devices"* ]]; then
            device=$(echo "$line" | awk '{print $4}')
            log "Обнаружено USB-устройство: $device"

            # Создание тестового файла (например, 100MB)
            test_file="/tmp/test_file"
            dd if=/dev/zero of="$test_file" bs=1M count=100
            log "Создан тестовый файл: $test_file"

            # Запись тестового файла на флешку
            log "Запись тестового файла на флешку..."
            start_time=$(date +%s)
            dd if="$test_file" of="$device/test_file" bs=1M
            end_time=$(date +%s)
            duration=$((end_time - start_time))
            log "Запись завершена. Затраченное время: $duration секунд."

            # Удаление тестового файла
            rm "$test_file"

            # Считывание тестового файла с флешки
            log "Считывание тестового файла с флешки..."
            start_time=$(date +%s)
            dd if="$device/test_file" of="$test_file" bs=1M
            end_time=$(date +%s)
            duration=$((end_time - start_time))
            log "Считывание завершено. Затраченное время: $duration секунд."

            # Удаление тестового файла с флешки
            rm "$device/test_file"

            log "Работа завершена."
        fi
    done
done


