﻿Elvees Testing Platform v0.0.3 - платформа для проведения тестирования модулей устройств. В данный момент находится в стадии beta.

Для работы с платформой необходимо запустить в консоли TUI меню платформы:
"./menu.py"

Откроется меню с тестовой платформой. Во вкладке "Date" выбираем дату тестирования.

В списке необходимо выбрать нужный тест и нажать Enter.

CPU_Test - запускает тестирование процессора. Не отображает вывод терминала, поэтому после подтверждения выбора теста он запускается автоматически, программа останавливает работу через минуту и после выполнения отображает температуру.

Примечание: После проведения тестирования программа создает logfile.txt после каждого запуска теста программа обновляет данные. Данные: температура процессора каждую секунду итерации.

HardDisk – Программа запишет, отчистит кеш и считает созданный ей файл и в выводе отобразить скорость в mb/s

VideoPort – даёт информацию о видеовыходах и предоставляет информацию об их статусе.

Ethernet – получает информацию о доступных Ethernet интерфейсах и получает информацию об их статусе.

USB – запускает тест в ожидание, пользователь должен установить устройство в USB интерфейс. В случае исправности – тест завершится и в директории появится файл mount_log, в котором будет отображен путь и название устройства в USB интерфейсе

Для исправной работы программы необходимо установить дополнительные библиотеки, используемые платформой:

sudo pip3 install npyscreen subprocess os threading

sudo apt-get install lm-sensors

Внимание:

Перед запуском программы необходимо запустить root права (sudo su)

Когда появляется окно с уведомлением о старте тестирования – необходимо дождаться окна с результатом теста, окно с уведомлением закрывается, но не означает завершение теста, тест завершается только после того, как платформа выдаст результат.
