def immediate_call(func):
    return func()


@immediate_call
def kivymd_copy_dir():
    from pathlib import PurePath
    return PurePath(__file__).parent / 'kivymd_copy'


@immediate_call
def _use_the_local_copy_of_kivymd_if_the_official_one_is_not_installed():
    try:
        import kivymd
    except ImportError:
        import sys
        sys.path.append(str(kivymd_copy_dir))
    import kivymd


@immediate_call
def _register_icon_font_if_its_not():
    try:
        import kivymd.font_definitions
    except ImportError:
        from kivy.core.text import LabelBase
        if 'Icons' in LabelBase._fonts:
            return
        LabelBase.register(
            'Icons',
            str(kivymd_copy_dir.joinpath(
                'kivymd',
                'fonts',
                'materialdesignicons-webfont.ttf')))


from kivy.app import App


class IconViewerApp(App):

    def build(self):
        from os.path import join
        from iconviewer import IconViewer
        return IconViewer(
            savefile=join(self.user_data_dir, 'iconviewer.json'),
        )

    def on_stop(self):
        self.root.iv_save()


if __name__ == "__main__":
    IconViewerApp().run()
