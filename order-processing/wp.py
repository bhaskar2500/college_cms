from wpadmin.menu.menus import Menu

class MyMenu(Menu):
    """
    My super new menu ;)
    """
    def init_with_context(self, context):
        self.children += [
            items.MenuItem(
                title='Back to page',
                url='/',
                icon='fa-bullseye',
                css_styles='font-size: 1.5em;',
            ),
            items.AppList(
                title='Applications',
                icon='fa-tasks',
                exclude=('django.contrib.*',),
            ),
            items.ModelList(
                title='Auth models',
                icon='fa-tasks',
                models=('django.contrib.auth.*',),
            ),
            items.UserTools(
                css_styles='float: right;',
            ),
        ]
