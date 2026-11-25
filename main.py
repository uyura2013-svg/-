from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore

KV = """
ScreenManager:
    LockScreen:
    SettingsScreen:
<LockScreen>:
    name: "lock"
    BoxLayout:
        orientation: "vertical"
        padding: "28dp"
        spacing: "14dp"
        canvas.before:
            Color:
                rgba: (.025, .035, .06, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "[b]HARD LOCKER[/b]"
            markup: True
            font_size: "30sp"
            size_hint_y: .25
        Label:
            text: "ВВЕДИТЕ PIN-КОД"
            color: .55, .7, 1, 1
            size_hint_y: .1
        TextInput:
            id: pin_input
            password: True
            multiline: False
            input_filter: "int"
            hint_text: "••••"
            halign: "center"
            font_size: "28sp"
            size_hint_y: .14
            on_text_validate: root.unlock()
        Label:
            id: message
            text: "Устройство защищено"
            size_hint_y: .1
        GridLayout:
            cols: 3
            spacing: "10dp"
            size_hint_y: .4
            Button:
                text: "1"
                on_release: root.add_digit("1")
            Button:
                text: "2"
                on_release: root.add_digit("2")
            Button:
                text: "3"
                on_release: root.add_digit("3")
            Button:
                text: "4"
                on_release: root.add_digit("4")
            Button:
                text: "5"
                on_release: root.add_digit("5")
            Button:
                text: "6"
                on_release: root.add_digit("6")
            Button:
                text: "7"
                on_release: root.add_digit("7")
            Button:
                text: "8"
                on_release: root.add_digit("8")
            Button:
                text: "9"
                on_release: root.add_digit("9")
            Button:
                text: "⌫"
                on_release: root.backspace()
            Button:
                text: "0"
                on_release: root.add_digit("0")
            Button:
                text: "ОТКРЫТЬ"
                on_release: root.unlock()
<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        padding: "28dp"
        spacing: "16dp"
        Label:
            text: "[b]НАСТРОЙКИ[/b]"
            markup: True
            font_size: "26sp"
        TextInput:
            id: new_pin
            password: True
            multiline: False
            input_filter: "int"
            hint_text: "Новый PIN (4–8 цифр)"
            size_hint_y: .16
        Button:
            text: "СОХРАНИТЬ PIN"
            size_hint_y: .16
            on_release: root.save_pin()
        Label:
            id: status
            text: ""
        Button:
            text: "НАЗАД"
            size_hint_y: .16
            on_release: app.root.current = "lock"
"""
class LockScreen(Screen):
    def add_digit(self, digit):
        field = self.ids.pin_input
        if len(field.text) < 8:
            field.text += digit
    def backspace(self):
        self.ids.pin_input.text = self.ids.pin_input.text[:-1]
    def unlock(self):
        app = App.get_running_app()
        if self.ids.pin_input.text == app.store.get("security")["pin"]:
            self.ids.message.text = "PIN принят"
            self.ids.pin_input.text = ""
            app.root.current = "settings"
        else:
            self.ids.message.text = "Неверный PIN"
            self.ids.pin_input.text = ""
class SettingsScreen(Screen):
    def save_pin(self):
        value = self.ids.new_pin.text
        if not value.isdigit() or not 4 <= len(value) <= 8:
            self.ids.status.text = "Нужно от 4 до 8 цифр"
            return
        App.get_running_app().store.put("security", pin=value)
        self.ids.new_pin.text = ""
        self.ids.status.text = "PIN успешно изменён"
class HardLockerApp(App):
    def build(self):
        self.title = "HARD LOCKER"
        self.store = JsonStore(self.user_data_dir + "/locker.json")
        if not self.store.exists("security"):
            self.store.put("security", pin="1467")
        return Builder.load_string(KV)
if __name__ == "__main__":
    HardLockerApp().run()
