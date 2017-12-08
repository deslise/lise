from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from django.utils.translation import ugettext_lazy as _

from liseadmin.dashboard_modules import RequestCategories


class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(modules.ModelList(
            _('Modelos'),
            exclude=('auth.*',),
            column=1,
            order=0,
            layout='inline',
        ))
        self.children.append(modules.AppList(
            _('Aplicações'),
            exclude=('auth.*',),
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            _('Ações Recentes'),
            limit=10,
            column=0,
            order=0
        ))
        self.children.append(RequestCategories(
           _('Solicitações de categoria'),
            column = 1,
            order=6
        ))