from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window

from SettingsJsonDB import SettingsJsonDB
from datetime import datetime
import webbrowser

import json

Window.size = (480, 750)


class StartScreen(MDScreen):
    pass


class SettingsScreen(MDFloatLayout):
    pass


class TabClasses(MDFloatLayout, MDTabsBase):
    pass


class TabDayWeek(MDAnchorLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    def build(self):
        self.JsonDB = SettingsJsonDB(r"data\app_data\settings.json")
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"  # Light
        self.theme_cls.primary_palette = "Green"
        self.scrolling_count = 0
        menu_items = [
            {
                "text": name_class,
                "on_release": lambda x=name_class: self.menu_callback(x),
            } for name_class in self.JsonDB.schedule_classes.keys()
        ]
        self.menu = MDDropdownMenu(items=menu_items)
        return StartScreen()

    def on_start(self):
        for name_class in self.JsonDB.schedule_classes.keys():
            self.root.ids.tabs_classes.add_widget(TabClasses(title=name_class, id=name_class))
        self.root.ids.tabs_classes.switch_tab(self.JsonDB.default_class)
        self.data_whith_change_class = self.JsonDB.schedule_classes[self.JsonDB.default_class]
        # self.root.ids.tabs_classes.get_current_tab() - класс активной вкладки
        # print(self.root.ids.tabs_classes.get_tab_list())

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if self.scrolling_count > 0:
            list_tabs = instance_tab.ids.tabs_day_week.get_tab_list()
            if len(list_tabs) < len(self.JsonDB.days):
                for day in self.JsonDB.days:
                    instance_tab.ids.tabs_day_week.add_widget(TabDayWeek(title=day))

            instance_tab.ids.tabs_day_week.switch_tab(self.JsonDB.days[datetime.now().weekday() % 6])
            self.data_whith_change_class = self.JsonDB.schedule_classes[tab_text]
            self.active_groupe = tab_text
        self.scrolling_count += 1

    def on_datatable(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.data_for_day = self.data_whith_change_class[self.JsonDB.days.index(tab_text)]
        self.table = MDDataTable(use_pagination=True,
                                 background_color_header="#65275d",
                                 background_color_cell="#451938",
                                 background_color_selected_cell="e4514f",
                                 rows_num=10,
                                 column_data=[('№', dp(10)),
                                              ('Время', dp(30)),
                                              ('Предмет', dp(40))],
                                 row_data=[(number + 1, lesson[0], lesson[1]) for number, lesson in
                                           enumerate(self.data_for_day)])
        instance_tab.add_widget(self.table)
        print(self.active_groupe, tab_text)

    def open_github(self):
        webbrowser.open('https://github.com/Nikolay1562005', new=2)

    def open_telegram(self):
        webbrowser.open('https://t.me/kolya_shmykov', new=2)

    def settings(self, dots_vertical):
        self.menu.caller = dots_vertical
        self.menu.open()

    def update(self):
        self.JsonDB.update_from_table()
        self.JsonDB.to_json()


    def menu_callback(self, text_item):
        pass


if __name__ in ('__main__', '__android__'):
    MainApp().run()