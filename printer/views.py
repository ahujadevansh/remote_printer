from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# pylint: disable=unused-import
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from remote_printer.users.models import CustomUser

from . import forms
from . models import PrintRequest, PrintRequestFile





class PrintRequestCreateView(LoginRequiredMixin, View):

    template_name = 'printer/print_request_create.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request_form = forms.PrintRequestForm()
        formset = forms.PrintRequestFileFormSet()
        context = {'print_request_form': print_request_form,
                   'formset': formset
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request_form = forms.PrintRequestForm(request.POST)
        formset = forms.PrintRequestFileFormSet(request.POST, request.FILES)
        if print_request_form.is_valid() and formset.is_valid():
            if print_request_form.instance.description or len(formset) != 0:
                print_request_form.instance.client = self.request.user
                print_request_form.instance.status = PrintRequest.STATUS.get_value('requested')
                print_request = print_request_form.save()

                for form in formset:
                    if form.instance.document:
                        form.instance.print_request_id = print_request
                        form.save()

                return redirect(print_request)
            else:
                messages.warning(request, "Please Fill either Description or submit a file")

        context = {'print_request_form': print_request_form,
                   'formset': formset
                   }
        return render(request, self.template_name, context)


class UserPrintRequestListView(LoginRequiredMixin, ListView):

    template_name = 'printer/user_print_request_list.html'
    model = PrintRequest
    context_object_name = 'prints'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.request.user.pk)
        return PrintRequest.objects.filter(Q(client=user) & Q(is_deleted=False)).order_by('-created_at')

class UserPrintRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, View):

    template_name = 'printer/user_print_request_detail.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = PrintRequest.objects.filter(Q(pk=self.kwargs.get('pk')) & Q(is_deleted=False)).first()
        print_requests_files = PrintRequestFile.objects.filter(Q(print_request_id=print_request.pk) &
                                                               Q(is_deleted=False))
        print(print_requests_files)
        if print_request:
            context = {'print_request': print_request,
                       'print_requests_files': print_requests_files
                      }
            return render(request, self.template_name, context)

        return HttpResponse("<h1>404</h1>")


    def test_func(self):
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.client == self.request.user:
            return True
        return False

class PrintRequestSoftDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.status in (3, 4, 5):
            print_request.is_deleted = True
            print_request.save()
            print_requests_files = PrintRequestFile.objects.filter(pk=self.kwargs.get('pk'))
            for print_requests_file in print_requests_files:
                print_requests_file.is_deleted = True
                print_requests_file.save()
            messages.info(request, "Your print request has been successfully deleted")
        else:
            messages.error(request, "Your print request cannot be deleted")
        return redirect(print_request)

    def test_func(self):
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.client == self.request.user:
            return True
        return False

class PrintRequestCancelView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.status == 1:
            print_request.status = print_request.STATUS.get_value("cancelled")
            print_request.save()
            messages.info(request, "Your print request has been cancelled deleted")
        else:
            messages.error(request, "Your print request cannot be cancelled")
        return redirect(print_request)

    def test_func(self):
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.client == self.request.user:
            return True
        return False

class PrintRequestRejectView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.status == 1:
            print_request.status = print_request.STATUS.get_value("rejected")
            print_request.save()
            messages.info(request, "Your print request has been rejected")
        else:
            messages.error(request, "Your print request cannot be rejected")
        return redirect(print_request)

    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
            return True
        return False

class PrintRequestReapplyView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.status == 4:
            print_request.status = print_request.STATUS.get_value("requested")
            print_request.save()
            messages.info(request, "Your print request has been re applied")
        else:
            messages.error(request, "Your print request cannot be re applied")
        return redirect(print_request)

    def test_func(self):
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.client == self.request.user:
            return True
        return False
