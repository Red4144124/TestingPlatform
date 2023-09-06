#!/usr/bin/env python

import subprocess
import os
import curses

devices = {
    "Device 1": {
        "tests": [
            {"name": "Тестирование процессора", "command": "Cpu_Test.sh"},
            {"name": "Проверка Ethernet интерфейсов", "command": "Ethernet.sh"},
            {"name": "Тестирование накопителя", "command": "HardDisk.sh"},
            {"name": "Проверка видео-интерфейсов", "command": "VideoPort.sh"},
            {"name": "USB интерфейсы", "command": "USB.sh"}
        ]
    },
    "Device 2": {
        "tests": [
            {"name": "Test 1 Python", "command": "test3.py"},
            {"name": "Test 2 Bash", "command": "test4.sh"}
        ]
    }
    # Add another tests
}

program_title = "Elvees Testing Platform v0.0.4"

def draw_menu(stdscr, options, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, program_title, curses.A_STANDOUT)
    for idx, option in enumerate(options):
        x = 2
        y = idx + 2
        if idx == selected_row:
            stdscr.addstr(y, x, f"> {option}", curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, f"  {option}")
    
    help_text = "Используйте стрелки для навигации, Enter для выбора, Ctrl+T для возвращения в предыдущее меню, два раза нажмите Esc для закрытия программы."
    stdscr.addstr(h - 2, 0, help_text, curses.A_STANDOUT)
    stdscr.refresh()

def execute_cmd(stdscr, cmd_filename):
    stdscr.clear()
    stdscr.addstr(0, 0, program_title, curses.A_STANDOUT)
    stdscr.addstr(2, 2, "Executing command...")
    stdscr.refresh()

    script_path = os.path.join(os.path.dirname(__file__), cmd_filename)
    
    console_height = curses.LINES // 2
    console_width = curses.COLS // 2
    console_win = curses.newwin(console_height, console_width, curses.LINES // 4, curses.COLS // 4)
    console_win.scrollok(True)
    
    console_border = curses.newwin(console_height + 2, console_width + 2, curses.LINES // 4 - 1, curses.COLS // 4 - 1)
    console_border.box()
    
    stdscr.clear()
    stdscr.addstr(0, 0, program_title, curses.A_STANDOUT)
    stdscr.addstr(2, 2, "Идёт выполнение теста...")
    stdscr.refresh()
    
    try:
        process = subprocess.Popen(script_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdscr.addstr(4, 2, "Процесс тестирования:")
        stdscr.addstr(5, 2, "-------------")
        stdscr.refresh()
        
        while process.poll() is None:
            line = process.stdout.readline()
            if line:
                console_win.addstr(line)
                console_win.refresh()
                console_border.refresh()

        stdscr.addstr(5, 2, "-------------")
        stdscr.addstr(6, 2, "Тест выполнен.")
        stdscr.addstr(7, 2, "Нажмите любую клавишу...")
        stdscr.refresh()
        stdscr.getch()
    
    except Exception as e:
        stdscr.addstr(4, 2, f"Ошибка: {str(e)}")
        stdscr.addstr(5, 2, "Нажмите любую клавишу...")
        stdscr.refresh()
        stdscr.getch()

    stdscr.clear()
    stdscr.addstr(0, 0, program_title, curses.A_STANDOUT)
    stdscr.addstr(2, 2, f"Тест завершён с кодом: {process.returncode}")
    stdscr.addstr(3, 2, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    current_menu = devices
    selected_row = 0

    while True:
        if isinstance(current_menu, dict):
            options = list(current_menu.keys())
        else:
            options = [test["name"] for test in current_menu]

        draw_menu(stdscr, options, selected_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(options) - 1:
            selected_row += 1
        elif key == ord('\n'):
            if isinstance(current_menu, dict):
                selected_device = options[selected_row]
                current_menu = current_menu[selected_device]["tests"]
                selected_row = 0
            else:
                selected_test = current_menu[selected_row]
                execute_cmd(stdscr, selected_test["command"])
        elif key == 20:  # Ctrl + T
            if isinstance(current_menu, list):
                current_menu = devices
                selected_row = 0
        elif key == 27:  # Esc
            break  # Выход из цикла и закрытие программы

if __name__ == "__main__":
    curses.wrapper(main)

