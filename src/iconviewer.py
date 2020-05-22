__all__ = ('IconViewer', )

from functools import lru_cache
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import (
    StringProperty, OptionProperty, ColorProperty, NumericProperty,
    ObjectProperty,
)
from kivy.utils import get_color_from_hex
from kivy.clock import Clock


colors = {
    'white': get_color_from_hex("#FFFFFF"),
    'red': get_color_from_hex("#FF5555"),
    'green': get_color_from_hex("#00FF00"),
    'blue': get_color_from_hex("#7777FF"),
}
next_group = {
    'white': 'red',
    'red': 'green',
    'green': 'blue',
    'blue': 'white',
}


Builder.load_string('''
#:import md_icons kivymd.icon_definitions.md_icons
#:set ICON_SIZE 64
#:import colors iconviewer.colors
#:import next_group iconviewer.next_group
#:import Factory kivy.factory.Factory
#:import partial functools.partial
#:import Clock kivy.clock.Clock
#:import NoTransition kivy.uix.screenmanager.NoTransition

<IVIcon>:
    font_name: 'Icons'
    text: md_icons.get(self.icon, '')

<IVIconButton@ButtonBehavior+IVIcon>:

<IconViewer>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    IVTabs:
        id: tabs
        size_hint_y: None
        height: dp(40)
        spacing: 20
        padding: 20, 0
        line_color: .2, .2, .2, 1
        line_width: 2
        IVTabHeader:
            group: 'tab'
            name: 'all'
            text: 'All'
            font_size: 20
            on_state: if args[1] == 'down': scrmgr.current = 'all'
        IVTabHeader:
            group: 'tab'
            name: 'red'
            color: colors['red']
            font_name: 'Icons'
            font_size: 30
            text: md_icons['star']
            on_state: if args[1] == 'down': scrmgr.current = 'red'
        IVTabHeader:
            group: 'tab'
            name: 'green'
            color: colors['green']
            font_name: 'Icons'
            font_size: 30
            text: md_icons['star']
            on_state: if args[1] == 'down': scrmgr.current = 'green'
        IVTabHeader:
            group: 'tab'
            name: 'blue'
            color: colors['blue']
            font_name: 'Icons'
            font_size: 30
            text: md_icons['star']
            on_state: if args[1] == 'down': scrmgr.current = 'blue'
    ScreenManager:
        id: scrmgr
        transition: NoTransition()
        Screen:
            name: 'blank'
        Screen:
            name: 'all'
            on_pre_leave: root.iv_update(rv_all.data)
            on_enter:
                rv_all.iv_update(
                root._savedata,
                filter=lambda icon, group: ti_filter.text in icon
                )
            BoxLayout:
                orientation: 'vertical'
                spacing: 10
                IVGridRV:
                    id: rv_all
                BoxLayout:
                    size_hint_y: None
                    height: max(sp(15), 30)
                    IVIcon:
                        size_hint_x: None
                        width: max(sp(15), 30)
                        font_size: max(sp(15), 30)
                        color: 1, 1, 1, 1
                        icon: 'file-find-outline'
                    TextInput:
                        id: ti_filter
                        multiline: False
                        on_text_validate:
                            root.iv_update(rv_all.data)
                            rv_all.iv_update(
                            root._savedata,
                            filter=lambda icon, group: ti_filter.text in icon
                            )
                            Clock.schedule_once(lambda __: setattr(self, 'focus', True), .3)
        Screen:
            name: 'red'
            on_pre_leave: root.iv_update(rv_red.data)
            on_enter:
                rv_red.iv_update(
                root._savedata,
                filter=lambda icon, group: group == 'red'
                )
            IVBoxRV:
                id: rv_red
        Screen:
            name: 'green'
            on_pre_leave: root.iv_update(rv_green.data)
            on_enter:
                rv_green.iv_update(
                root._savedata,
                filter=lambda icon, group: group == 'green'
                )
            IVBoxRV:
                id: rv_green
        Screen:
            name: 'blue'
            on_pre_leave: root.iv_update(rv_blue.data)
            on_enter:
                rv_blue.iv_update(
                root._savedata,
                filter=lambda icon, group: group == 'blue'
                )
            IVBoxRV:
                id: rv_blue


<IVGridViewClass@IVBaseViewClass+IVIconButton>:
    font_size: ICON_SIZE
    color: colors[root.group]
    size_hint_min: ICON_SIZE, ICON_SIZE
    on_press:
        print(root.icon)
        next = next_group[root.group]
        root.group = next
        root.rv.data[root.get_data_index()]['group'] = next

<IVGridRV@IVRecycleView>:
    viewclass: 'IVGridViewClass'
    scroll_type: ['bars', 'content']
    bar_width: 20
    RecycleGridLayout:
        cols: int(self.width) // (ICON_SIZE + 20)
        size_hint_y: None
        height: self.minimum_height
        default_size_hint: None, None
        default_size: (ICON_SIZE + 20), (ICON_SIZE + 20)

<IVBoxViewClass@IVBaseViewClass+BoxLayout>:
    spacing: 20
    IVIconButton:
        size_hint_x: None
        width: ICON_SIZE
        font_size: ICON_SIZE
        color: colors[root.group]
        icon: root.icon
        on_press:
            print(root.icon)
            next = next_group[root.group]
            root.group = next
            root.rv.data[root.get_data_index()]['group'] = next
    Label:
        text: root.icon
        font_size: max(20, sp(15))

<IVBoxRV@IVRecycleView>:
    viewclass: 'IVBoxViewClass'
    scroll_type: ['bars', 'content']
    bar_width: 20
    RecycleBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        default_size_hint: 1, None
        default_size: 100, ICON_SIZE
''')


class IVIcon(Factory.Label):
    icon = StringProperty()


class IVTabHeader(Factory.ToggleButtonBehavior, Factory.Label):
    name = StringProperty()

    def on_state(self, __, state):
        if state == 'down':
            self.parent.iv_highlight(self)


class IVTabs(Factory.BoxLayout):
    line_color = ColorProperty("#FFFFFF")
    line_width = NumericProperty(1.0)
    _next_highlight = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        from kivy.graphics import InstructionGroup, Color, Line, Quad
        self._inst_group = InstructionGroup()
        self._inst_color = Color()
        self._inst_line = Line()
        self._inst_group.add(self._inst_color)
        self._inst_group.add(self._inst_line)
        self._current_highlight = None
        super().__init__(**kwargs)
        self._trigger_update_points = Clock.create_trigger(self._iv_update_points, 0)
        trigger = Clock.create_trigger(self._iv_rebind, 0)
        self.fbind('_next_highlight', trigger)
        trigger()

    def on_line_color(self, __, color):
        self._inst_color.rgba = color

    def on_line_width(self, __, width):
        self._inst_line.width = width

    def iv_unhighlight(self):
        self._next_highlight = None

    def iv_highlight(self, widget):
        widget = widget.__self__
        if widget is self._current_highlight:
            return
        if widget not in self.children:
            raise ValueError(f"{widget!r} is not a child of mine.")
        self._next_highlight = widget

    def remove_widget(self, child, *args, **kwargs):
        if child.__self__ is self._current_highlight:
            self._next_highlight = None
        return super().remove_widget(child, *args, **kwargs)

    def _iv_rebind(self, *args):
        trigger = self._trigger_update_points
        current = self._current_highlight
        next = self._next_highlight
        if current is not None:
            self.canvas.before.remove(self._inst_group)
            current.unbind(pos=trigger, size=trigger)
            self._current_highlight = None
        if next is None:
            self.unbind(pos=trigger, size=trigger)
            return
        next.bind(pos=trigger, size=trigger)
        self._current_highlight = next
        self.canvas.before.add(self._inst_group)
        trigger()

    def _iv_update_points(self, *args):
        spacing = self.spacing
        cur = self._current_highlight
        y = self.y
        top = self.top
        cur_x = cur.x
        cur_right = cur.right
        self._inst_line.points = [
            *self.pos,
            cur_x - spacing, y,
            cur_x, top,
            cur_right, top,
            cur_right + spacing, y,
            self.right, y,
        ]


class IVBaseViewClass:
    icon = StringProperty()
    group = OptionProperty('white', options=('white', 'red', 'green', 'blue'))

    @property
    def rv(self):
        return self.parent.parent

    def get_data_index(self):
        return self.parent.get_view_index_at(self.center)
Factory.register('IVBaseViewClass', cls=IVBaseViewClass)


class IVRecycleView(Factory.RecycleView):
    def iv_update(self, data, *, filter):
        from kivymd.icon_definitions import md_icons
        self.data = (
            {'icon': icon, 'group': data[icon], }
            for icon in md_icons if filter(icon, data[icon])
        )


class IconViewer(Factory.BoxLayout):
    savefile = StringProperty()

    def on_kv_post(self, *args, **kwargs):
        self.iv_load()
        try:
            initial_tab = next(iter(self._savedata.values()))
        except StopIteration:
            initial_tab = 'all'
        for tab in self.ids.tabs.children:
            if tab.name == initial_tab:
                tab.state = 'down'
                break
        

    def iv_load(self):
        from pathlib import Path
        from collections import defaultdict
        import json

        self._savedata = defaultdict(lambda: 'white')
        if not self.savefile:
            return
        savefile = Path(self.savefile)
        if savefile.exists():
            self._savedata.update(
                json.loads(savefile.read_text(encoding='utf8'))
            )

    def iv_save(self):
        import json
        from pathlib import Path

        if not self.savefile:
            return
        self.ids.scrmgr.current = 'blank'
        data = {
            icon: group for icon, group in self._savedata.items()
            if group != 'white'
        }
        Path(self.savefile).write_text(json.dumps(data), encoding='utf8')

    def iv_update(self, rv_data):
        self._savedata.update(
            {datum['icon']: datum['group'] for datum in rv_data}
        )
