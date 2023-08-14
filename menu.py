#!/usr/bin/env python3

# Copyright 2023 RnD Center "ELVEES", JSC

import npyscreen
import subprocess
import os
import threading

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("DEVICE", DeviceForm, name="Выберите устройство")
        self.addForm("MAIN", MainForm, name="Тестовая платформа Elvees v0.0.1")
        self.addForm("TERMINAL", TerminalForm, name="ТЕРМИНАЛ")
        self.selected_device = None

class TestSelect(npyscreen.MultiLineAction):
    def __init__(self, *args, **kwargs):
        self.parentApp = kwargs.pop('parentApp', None)
        self.device_tests = kwargs.pop('device_tests', [])
        super(TestSelect, self).__init__(*args, **kwargs)

    def actionHighlighted(self, act_on_this, keypress):
        if self.parentApp.selected_device is None:
            npyscreen.notify_confirm("Пожалуйста, сначала выберите устройство.", title="Ошибка", form_color='STANDOUT')
            return

        # Take the name of the file
        test_file_py = act_on_this + ".py"
        test_file_sh = act_on_this + ".sh"

        # Check the file with test
        if os.path.exists(test_file_py):
            # Starting Python test in a separate thread
            threading.Thread(target=self.run_test, args=(["python3", test_file_py],)).start()
        elif os.path.exists(test_file_sh):
            # Starting Shell test in a separate thread
            threading.Thread(target=self.run_test, args=(["sh", test_file_sh],)).start()
        else:
            npyscreen.notify_confirm(f"Тест '{act_on_this}' не доступен.", title="Ошибка", form_color='STANDOUT')
            return

    def when_cancelled(self):
        self.parentApp.switchForm("MAIN")

    def when_value_edited(self):
        self.parentApp.switchForm("MAIN")

    def run_test(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, universal_newlines=True)
        stdout, stderr = process.communicate()
        output_text = f"Вывод терминала:\n{stdout}\n\nВывод ошибок:\n{stderr}"
        self.parentApp.getForm('TERMINAL').update_terminal_output(output_text)
        self.parentApp.switchForm('TERMINAL')

class TerminalForm(npyscreen.ActionPopup):
    def create(self):
        self.output_buffer = self.add(npyscreen.BufferPager, autowrap=True)

    def update_terminal_output(self, output_text):
        self.output_buffer.values = output_text.splitlines()
        self.output_buffer.display()

    def on_ok(self):
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

class MainForm(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.TitleDateCombo, name="Дата:", max_width=self.useable_space()[1] // 2)
        self.add(npyscreen.ButtonPress, name="Выбрать устройство", when_pressed_function=self.choose_device)
        self.test_choices = self.add(TestSelect, name="Выберите тест", values=[], parentApp=self.parentApp, scroll_exit=True)

    def whenResize(self):
        super(MainForm, self).whenResize()
        self.test_choices.width = self.useable_space()[1]

    def beforeEditing(self):
        if self.parentApp.selected_device is not None:
            test_values = self.get_tests_for_device(self.parentApp.selected_device)
            self.test_choices.values = test_values

    def get_tests_for_device(self, device):
        # Здесь вам нужно определить и вернуть список тестов для выбранного устройства
        if device == "Тонкий Клиент":
            return ["Cpu_Test", "HardDisk", "RAM_test"]
        elif device == "Смартфон-Спутник":
            return ["Cpu_Test", "HardDisk", "RAM_test"]
        elif device == "Планшет-Победа":
            return ["Cpu_Test", "HardDisk", "RAM_test"]
        elif device == "Навигатор":
            return ["Cpu_Test", "HardDisk", "RAM_test"]
        else:
            return []

    def choose_device(self):
        self.parentApp.switchForm("DEVICE")

class DeviceForm(npyscreen.ActionForm):
    def create(self):
        self.devices = ["Тонкий Клиент", "Смартфон-Спутник", "Планшет-Победа", "Навигатор"]
        self.device_select = self.add(npyscreen.TitleSelectOne, name="Список устройств:", max_height=4, values=self.devices)

    def on_ok(self):
        self.parentApp.selected_device = self.devices[self.device_select.value[0]]
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm(None)

if __name__ == '__main__':
    MyApp = App()
    MyApp.run()