from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        context = {'sidebarSection': 'home'}
        return render(request, self.template_name, context)
