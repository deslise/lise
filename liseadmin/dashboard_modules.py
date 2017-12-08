from jet.dashboard.modules import DashboardModule

from managedata.models import RequestCategory


class RequestCategories(DashboardModule):
    title = 'Solicitações de categoria'
    # title_url = '/admin/request_categories/'
    template = 'request-categories-widgets.html'
    deletable = True

    def init_with_context(self, context):
        self.children = RequestCategory.objects.filter(status='pendente').order_by('-date_request')