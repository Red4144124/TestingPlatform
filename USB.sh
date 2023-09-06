#!/bin/bash

# Определите имя файла журнала
log_file="mount_log.txt"

# Очистите или создайте файл журнала
> "$log_file"

mount_old="$(mount)"
mount_new="${mount_old}"

while [[ "${mount_new}" == "${mount_old}" ]]; do
    sleep 1
    mount_new="$(mount)"
done

# Получите добавленные строки смонтированных устройств, используя sort и uniq
added_lines=$(sort <(echo "${mount_old}") <(echo "${mount_new}") | uniq -u | awk '{ print $3 }')

# Запись добавленных строк в файл журнала
echo "$added_lines" >> "$log_file"

# Вывод добавленных строк на стандартный вывод (консоль)
echo "$added_lines"

# Дополнительно можно использовать diff и grep для поиска различий
# added_lines=$(diff <(echo "${mount_old}") <(echo "${mount_new}") | grep ">" | awk '{ print $4 }')

# Записать добавленные строки в файл журнала
# echo "$added_lines" >> "$log_file"


