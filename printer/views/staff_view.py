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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import strip_tags

from remote_printer.users.models import CustomUser

from printer import forms as printer_forms
from printer.models import PrintRequest, PrintRequestFile, Price



class StaffPrintRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    template_name = 'printer/staff_print_request_list_table.html'
    model = PrintRequest
    context_object_name = 'prints'
    flag = 1


    def get_queryset(self):
        status = self.kwargs.get('status', 'requested')
        if status == 'deleted':
            return PrintRequest.objects.filter(Q(is_deleted=True)).order_by('-created_at')
        else:
            status = PrintRequest.STATUS.get_value(status)
            return PrintRequest.objects.filter(Q(status=status) &
                                           Q(is_deleted=False)).order_by('-created_at')


    def get_context_data(self, **kwargs):
        # pylint: disable=arguments-differ
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if self.flag:
            self.template_name = 'printer/staff_print_request_list.html'
            context['sidebarSection'] = 'staff_print_request_list'
        context['status'] = self.kwargs.get('status', 'requested')
        return context

    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
            return True
        return False

class StaffPrintRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, View):

    template_name = 'printer/staff_print_request_detail.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = PrintRequest.objects.filter(Q(pk=self.kwargs.get('pk')) & Q(is_deleted=False)).first()
        if print_request:
            print_requests_files = PrintRequestFile.objects.filter(Q(print_request=print_request.pk) &
                                                                   Q(is_deleted=False)
                                                                   )
            form = printer_forms.StaffPrintRequestForm(instance=print_request)

            context = {'print_request': print_request,
                       'print_requests_files': print_requests_files,
                       'form': form,
                       'sidebarSection': 'staff_print_request_detail',
                      }
            return render(request, self.template_name, context)

        return HttpResponse("<h1>404</h1>")

    def post(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = PrintRequest.objects.filter(Q(pk=self.kwargs.get('pk')) & Q(is_deleted=False)).first()
        print_requests_files = PrintRequestFile.objects.filter(Q(print_request=print_request.pk) &
                                                               Q(is_deleted=False))
        form = printer_forms.StaffPrintRequestForm(self.request.POST, instance=print_request)

        if form.is_valid():

            if print_request.status in (1, 2):
                form.instance.status = PrintRequest.STATUS.get_value('printed')
                price = Price.objects.latest('wef')
                form.instance.printed_on = timezone.now()

                price = (
                    form.instance.no_of_bnw_page * price.bnw_page +
                    form.instance.no_of_color_page * price.color_pages +
                    (
                        form.instance.no_of_page +
                        form.instance.no_of_front_page +
                        form.instance.no_of_blank_page
                    ) * price.page
                )

                if bool(price):
                    form.instance.amount = price
                else:
                    form.instance.amount = 1

                form.save()
                return redirect('printer:staff_print_request_list', status='printed')
            else:
                return HttpResponse("<h1>404</h1>")
        else:
            context = {'print_request': print_request,
                       'print_requests_files': print_requests_files,
                       'form': form,
                       'sidebarSection': 'staff_print_request_detail',
                      }
            return render(request, self.template_name, context)



    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
            return True
        return False


class PrintRequestRejectView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.status == 1:
            print_request.status = print_request.STATUS.get_value("rejected")
            print_request.rejected_on = timezone.now()
            print_request.save()
        else:
            messages.error(request, "Your print request cannot be rejected")
        return redirect('printer:staff_print_request_list', status='rejected')

    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
            return True
        return False

class PrintRequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = get_object_or_404(PrintRequest, pk=self.kwargs.get('pk'))
        if print_request.is_deleted:
            print_requests_files = PrintRequestFile.objects.filter(print_request=self.kwargs.get('pk'))
            for print_requests_file in print_requests_files:
                print_requests_file.delete()
            print_request.delete()
            messages.info(request, "Your print request has been successfully deleted")
        else:
            messages.error(request, "Your print request cannot be deleted")
        return redirect('printer:staff_print_request_list', status='deleted')

    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
            return True
        return False
