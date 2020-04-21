from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum

from printer.models import PrintRequest

class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        user = self.request.user
        printed = PrintRequest.objects.filter(Q(client=user) &
                                              (Q(status=PrintRequest.STATUS.get_value('printed')) |
                                               Q(status=PrintRequest.STATUS.get_value('paid')))
                                             ).values('id').count()

        pending = PrintRequest.objects.filter(Q(client=user) & Q(status=PrintRequest.STATUS.get_value('requested'))
                                             ).values('id').count()

        paid = PrintRequest.objects.filter(Q(client=user) & Q(status=PrintRequest.STATUS.get_value('paid'))
                                          ).values('amount').aggregate(Sum('amount')).get('amount__sum', 0.00)

        unpaid = PrintRequest.objects.filter(Q(client=user) & Q(status=PrintRequest.STATUS.get_value('printed'))
                                            ).values('amount').aggregate(Sum('amount')).get('amount__sum', 0.00)
        context = {
            'sidebarSection': 'home',
            'printed': printed,
            'pending': pending,
            'paid': paid,
            'unpaid': unpaid,
            }
        return render(request, self.template_name, context)


def bad_request_view(request, *args, **kwargs):
    # pylint: disable=unused-argument
    response = render_to_response("400.html")
    response.status_code = 400
    return response

def page_not_found_view(request, *args, **kwargs):
    # pylint: disable=unused-argument
    response = render_to_response("404.html")
    response.status_code = 404
    return response

def permission_denied_view(request, *args, **kwargs):
    # pylint: disable=unused-argument
    response = render_to_response("403.html")
    response.status_code = 403
    return response

def error_view(request, *args, **kwargs):
    # pylint: disable=unused-argument
    response = render_to_response("500.html")
    response.status_code = 500
    return response
