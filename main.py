
import os
import json
import random

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

Window.clearcolor = get_color_from_hex("#101020")

STYLES = [
    "꧁༺ {} ༻꧂", "亗 {} 亗", "『 {} 』",
    "★彡 {} 彡★", "么 {} 么", "♛ {} ♛",
    "ツ {} ツ", "꧁ {} ꧂", "༒ {} ༒",
    "◥ {} ◤", "乂 {} 乂", "『ᴾᴿᴼ』{}",
    "♕ {} ♕", "⚡ {} ⚡", "✿ {} ✿",
    "☯ {} ☯", "𒆜 {} 𒆜", "᭄ {} ᭄",
    "♡ {} ♡", "彡 {} 彡"
]


class NickApp(App):

    def build(self):
        self.nicks = []
        self.favorites = []
        self.load_data()

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        root.add_widget(Label(
            text="[b]✦ NICK GENERATOR ✦[/b]",
            markup=True,
            font_size=27,
            color=(0.7, 0.5, 1, 1),
            size_hint_y=None,
            height=65
        ))

        self.name_input = TextInput(
            hint_text="Ismingizni yozing...",
            multiline=False,
            size_hint_y=None,
            height=55,
            font_size=19
        )
        root.add_widget(self.name_input)

        self.add_button(
            root, "✦ 20 TA NIK YARATISH",
            self.generate
        )

        self.add_button(
            root, "📋 BARCHASINI NUSXALASH",
            self.copy_all
        )

        self.add_button(
            root, "❤️ SEVIMLILAR",
            self.show_favorites
        )

        self.scroll = ScrollView()

        self.results = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        self.results.bind(
            minimum_height=self.results.setter("height")
        )

        self.scroll.add_widget(self.results)
        root.add_widget(self.scroll)

        return root

    def add_button(self, root, title, action):
        btn = Button(
            text=title,
            size_hint_y=None,
            height=52,
            background_color=(0.4, 0.2, 0.8, 1)
        )
        btn.bind(on_press=action)
        root.add_widget(btn)

    def generate(self, instance):
        name = self.name_input.text.strip()

        self.results.clear_widgets()
        self.nicks = []

        if not name:
            self.message("Avval ismingizni kiriting!")
            return

        styles = STYLES.copy()
        random.shuffle(styles)

        self.nicks = [
            style.format(name) for style in styles
        ]

        self.show_list(self.nicks)

    def show_list(self, items):
        self.results.clear_widgets()

        if not items:
            self.message("Hozircha niklar mavjud emas")
            return

        for nick in items:
            row = BoxLayout(
                size_hint_y=None,
                height=55,
                spacing=5
            )

            btn = Button(
                text=nick,
                background_color=(0.15, 0.15, 0.3, 1)
            )

            btn.bind(
                on_press=lambda b, n=nick:
                self.copy_nick(n)
            )

            fav = Button(
                text="❤️",
                size_hint_x=None,
                width=55
            )

            fav.bind(
                on_press=lambda b, n=nick:
                self.save_favorite(n)
            )

            row.add_widget(btn)
            row.add_widget(fav)

            self.results.add_widget(row)

    def copy_nick(self, nick):
        Clipboard.copy(nick)
        self.message("Nik nusxalandi!")

    def save_favorite(self, nick):
        if nick not in self.favorites:
            self.favorites.append(nick)
            self.save_data()
            self.message("Sevimlilarga saqlandi!")
        else:
            self.message("Bu nik allaqachon saqlangan!")

    def show_favorites(self, instance):
        self.show_list(self.favorites)

    def copy_all(self, instance):
        if self.nicks:
            Clipboard.copy("\n".join(self.nicks))
            self.message("20 ta nik nusxalandi!")
        else:
            self.message("Avval nik yarating!")

    def save_data(self):
        path = os.path.join(
            self.user_data_dir,
            "favorites.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.favorites,
                f,
                ensure_ascii=False
            )

    def load_data(self):
        path = os.path.join(
            self.user_data_dir,
            "favorites.json"
        )

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.favorites = json.load(f)
            except (OSError, json.JSONDecodeError):
                self.favorites = []

    def message(self, text):
        self.results.clear_widgets()

        self.results.add_widget(Label(
            text=text,
            size_hint_y=None,
            height=60
        ))


if __name__ == "__main__":
    NickApp().run()
