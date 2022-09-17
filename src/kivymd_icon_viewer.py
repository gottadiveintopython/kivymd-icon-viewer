__all__ = ('launch', 'KivyMDIconViewer', )

from functools import lru_cache

from kivy.utils import get_color_from_hex, reify
from kivy.properties import (
    ColorProperty, NumericProperty, ObjectProperty, OptionProperty, BooleanProperty, StringProperty, OptionProperty,
)
from kivy.graphics import InstructionGroup, Color, Line
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.lang import Builder

ToggleButtonBehavior = F.ToggleButtonBehavior
colors = {
    'white': get_color_from_hex("#FFFFFF"),
    'red': get_color_from_hex("#FF5555"),
    'green': get_color_from_hex("#00FF00"),
    'blue': get_color_from_hex("#7777FF"),
}
next_color_name = {
    'white': 'red',
    'red': 'green',
    'green': 'blue',
    'blue': 'white',
}
KV_CODE = '''
#:import md_icons kivymd.icon_definitions.md_icons
#:set ICON_SIZE 64
#:import colors kivymd_icon_viewer.colors
#:import next_color_name kivymd_icon_viewer.next_color_name
#:import Clock kivy.clock.Clock
#:import NoTransition kivy.uix.screenmanager.NoTransition

<IVIcon>:
    font_name: 'Icons'
    text: md_icons[self.icon]

<IVIconButton@ButtonBehavior+IVIcon>:
<IVTabs@IVTablikeLooksBehavior+BoxLayout>:

<KivyMDIconViewer>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    IVTabs:
        id: tabs
        size_hint_y: None
        height: dp(40)
        spacing: 20
        padding: 20, 0
        tab_line_color: .2, .2, .2, 1
        tab_line_width: 2
        IVTabHeader:
            group: 'tab'
            tab_name: 'all'
            text: 'All'
            font_size: 20
            on_state: if args[1] == 'down': scrmgr.current = 'all'
        IVTabHeader:
            group: 'tab'
            tab_name: 'red'
            color: colors['red']
            font_name: 'Icons'
            font_size: 30
            text: md_icons['star']
            on_state: if args[1] == 'down': scrmgr.current = 'red'
        IVTabHeader:
            group: 'tab'
            tab_name: 'green'
            color: colors['green']
            font_name: 'Icons'
            font_size: 30
            text: md_icons['star']
            on_state: if args[1] == 'down': scrmgr.current = 'green'
        IVTabHeader:
            group: 'tab'
            tab_name: 'blue'
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
                filter=lambda icon, color_name: ti_filter.text in icon
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
                            filter=lambda icon, color_name: ti_filter.text in icon
                            )
                            Clock.schedule_once(lambda __: setattr(self, 'focus', True), .3)
        Screen:
            name: 'red'
            on_pre_leave: root.iv_update(rv_red.data)
            on_enter:
                rv_red.iv_update(
                root._savedata,
                filter=lambda icon, color_name: color_name == 'red'
                )
            IVBoxRV:
                id: rv_red
        Screen:
            name: 'green'
            on_pre_leave: root.iv_update(rv_green.data)
            on_enter:
                rv_green.iv_update(
                root._savedata,
                filter=lambda icon, color_name: color_name == 'green'
                )
            IVBoxRV:
                id: rv_green
        Screen:
            name: 'blue'
            on_pre_leave: root.iv_update(rv_blue.data)
            on_enter:
                rv_blue.iv_update(
                root._savedata,
                filter=lambda icon, color_name: color_name == 'blue'
                )
            IVBoxRV:
                id: rv_blue

<IVGridViewClass@IVBaseViewClass+IVIconButton>:
    font_size: ICON_SIZE
    color: colors[root.color_name]
    size_hint_min: ICON_SIZE, ICON_SIZE
    on_press:
        print(root.icon)
        next = next_color_name[root.color_name]
        root.color_name = next
        root.rv.data[root.get_view_index()]['color_name'] = next

<IVGridRV@IVRecycleView>:
    viewclass: 'IVGridViewClass'
    scroll_type: ['bars', 'content']
    bar_width: 20
    always_overscroll: False
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
        color: colors[root.color_name]
        icon: root.icon
        on_press:
            print(root.icon)
            next = next_color_name[root.color_name]
            root.color_name = next
            root.rv.data[root.get_view_index()]['color_name'] = next
    Label:
        text: root.icon
        font_size: max(20, sp(15))

<IVBoxRV@IVRecycleView>:
    viewclass: 'IVBoxViewClass'
    scroll_type: ['bars', 'content']
    bar_width: 20
    always_overscroll: False
    RecycleBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        default_size_hint: 1, None
        default_size: 100, ICON_SIZE
'''


@lru_cache
def _load_kv():
    '''
    Kvコードの読み込みは本来moduleが読み込まれる時にやりたかったが、そうすると循環import系の問題が起きたのでやむなくこのようなやり方
    を採っている。
    '''
    Builder.load_string(KV_CODE)


class IVTablikeLooksBehavior:
    tab_style_h = OptionProperty('top', options=('top', 'bottom', ))
    tab_style_v = OptionProperty('left', options=('left', 'right'))
    tab_line_stays_inside = BooleanProperty(True)
    tab_line_color = ColorProperty("#FFFFFF")
    tab_line_width = NumericProperty(2)
    _tab_next_highlight = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self._tab_inst_color = Color()
        self._tab_inst_line = Line(joint='bevel', cap='square', width=2)
        self._tab_current_highlight = None
        super().__init__(**kwargs)
        inst_group = InstructionGroup()
        inst_group.add(self._tab_inst_color)
        inst_group.add(self._tab_inst_line)
        self.canvas.after.add(inst_group)
        self._tab_trigger_update_canvas = trigger_update_canvas = \
            Clock.create_trigger(self._tab_update_canvas_ver_inside, 0)
        self._tab_trigger_rebind = trigger_rebind = Clock.create_trigger(self._tab_rebind, 0)
        f = self.fbind
        f('pos', trigger_update_canvas)
        f('size', trigger_update_canvas)
        f('tab_line_width', trigger_update_canvas)
        f('spacing', trigger_update_canvas)
        f('padding', trigger_update_canvas)
        f('orientation', trigger_rebind)
        f('tab_style_h', trigger_rebind)
        f('tab_style_v', trigger_rebind)
        f('_tab_next_highlight', trigger_rebind)
        trigger_rebind()

    def on_tab_line_stays_inside(self, __, inside):
        t = self._tab_trigger_update_canvas
        t.callback = self._tab_update_canvas_ver_inside if inside else self._tab_update_canvas_ver_normal
        t.release()
        t()

    def on_tab_line_color(self, __, color):
        self._tab_inst_color.rgba = color

    def on_tab_line_width(self, __, width):
        self._tab_inst_line.width = width

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, ToggleButtonBehavior):
            widget.bind(state=self._on_tab_child_state)
        return super().add_widget(widget, *args, **kwargs)

    def remove_widget(self, widget, *args, **kwargs):
        if widget.__self__ is self._tab_current_highlight:
            self._tab_next_highlight = None
        if isinstance(widget, ToggleButtonBehavior):
            widget.unbind(state=self._on_tab_child_state)
        return super().remove_widget(widget, *args, **kwargs)

    def _on_tab_child_state(self, widget, state):
        self._tab_next_highlight = widget if state == 'down' else None

    def is_horizontal(boxlayout) -> bool:
        return boxlayout.orientation in ('horizontal', 'lr', 'rl')

    def _tab_rebind(self, *args):
        trigger = self._tab_trigger_update_canvas
        current = self._tab_current_highlight
        next = self._tab_next_highlight
        trigger()
        if current is not None:
            current.unbind(pos=trigger, size=trigger)
        self._tab_current_highlight = next
        if next is not None:
            next.bind(pos=trigger, size=trigger)

    def _tab_update_canvas_ver_normal(self, dt, is_horizontal=is_horizontal):
        spacing = self.spacing
        cur = self._tab_current_highlight
        inst_line = self._tab_inst_line
        is_horizontal = is_horizontal(self)
        y1 = self_y = self.y
        y2 = self_top = self.top
        x1 = self_x = self.x
        x2 = self_right = self.right
        if is_horizontal:
            if self.tab_style_h == 'bottom':
                y1, y2 = y2, y1
        else:
            if self.tab_style_v == 'left':
                x1, x2 = x2, x1
        if cur is None:
            inst_line.points = (self_x, y1, self_right, y1, ) if \
                is_horizontal else (x1, self_y, x1, self_top, )
        elif is_horizontal:
            cur_x = cur.x
            cur_right = cur.right
            inst_line.points = (
                self_x, y1,
                max(cur_x - spacing, self_x), y1,
                cur_x, y2,
                cur_right, y2,
                min(cur_right + spacing, self_right), y1,
                self_right, y1,
            )
        else:
            cur_y = cur.y
            cur_top = cur.top
            inst_line.points = (
                x1, self_y,
                x1, max(cur_y - spacing, self_y),
                x2, cur_y,
                x2, cur_top,
                x1, min(cur_top + spacing, self_top),
                x1, self_top,
            )

    def _tab_update_canvas_ver_inside(self, dt, is_horizontal=is_horizontal):
        spacing = self.spacing
        cur = self._tab_current_highlight
        inst_line = self._tab_inst_line
        is_horizontal = is_horizontal(self)
        lw = self.tab_line_width
        self_y = self.y + lw
        self_top = self.top - lw
        self_x = self.x + lw
        self_right = self.right - lw
        y1 = self_y
        y2 = self_top
        x1 = self_x
        x2 = self_right
        if is_horizontal:
            if self.tab_style_h == 'bottom':
                y1, y2 = y2, y1
        else:
            if self.tab_style_v == 'left':
                x1, x2 = x2, x1
        if cur is None:
            inst_line.points = (self_x, y1, self_right, y1, ) if \
                is_horizontal else (x1, self_y, x1, self_top, )
        elif is_horizontal:
            cur_x = cur.x + lw
            cur_right = cur.right - lw
            inst_line.points = (
                self_x, y1,
                max(cur_x - spacing, x1), y1,
                cur_x, y2,
                cur_right, y2,
                min(cur_right + spacing, x2), y1,
                self_right, y1,
            )
        else:
            cur_y = cur.y + lw
            cur_top = cur.top - lw
            inst_line.points = (
                x1, self_y,
                x1, max(cur_y - spacing, y1),
                x2, cur_y,
                x2, cur_top,
                x1, min(cur_top + spacing, y2),
                x1, self_top,
            )


class IVIcon(F.Label):
    icon = StringProperty('blank')


class IVTabHeader(F.ToggleButtonBehavior, F.Label):
    tab_name = StringProperty()


class IVBaseViewClass:
    icon = StringProperty('blank')
    color_name = OptionProperty('white', options=tuple(next_color_name))

    @reify
    def rv(self):
        return self.parent.recycleview

    def get_view_index(self):
        return self.parent.get_view_index_at(self.center)


class IVRecycleView(F.RecycleView):
    def iv_update(self, data, *, filter):
        from kivymd.icon_definitions import md_icons
        self.data = (
            {'icon': icon, 'color_name': data[icon], }
            for icon in md_icons if filter(icon, data[icon])
        )


class KivyMDIconViewer(F.BoxLayout):
    savefile = StringProperty()

    def __init__(self, **kwargs):
        _load_kv()
        super().__init__(**kwargs)

    def on_kv_post(self, *args, **kwargs):
        self.iv_load()
        initial_tab = next(iter(self._savedata.values()), 'all')
        for tab in self.ids.tabs.children:
            if tab.tab_name == initial_tab:
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
            icon: color_name for icon, color_name in self._savedata.items()
            if color_name != 'white'
        }
        Path(self.savefile).write_text(json.dumps(data), encoding='utf8')

    def iv_update(self, rv_data):
        self._savedata.update(
            {datum['icon']: datum['color_name'] for datum in rv_data}
        )


F.register('IVTablikeLooksBehavior', cls=IVTablikeLooksBehavior)
F.register('IVBaseViewClass', cls=IVBaseViewClass)


def launch():
    from kivy.app import App

    class IconViewerApp(App):

        def build(self):
            from os.path import join
            return KivyMDIconViewer(
                savefile=join(self.user_data_dir, 'iconviewer.json'),
            )

        def on_stop(self):
            self.root.iv_save()

    IconViewerApp(title='KivyMD Icon Viewer').run()
