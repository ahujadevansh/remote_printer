import datetime

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
from django.utils.html import strip_tags
from remote_printer.users.models import CustomUser

from . import forms as printer_forms
from . models import PrintRequest, PrintRequestFile, Price



class PrintRequestCreateView(LoginRequiredMixin, View):

    template_name = 'printer/print_request_create.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request_form = printer_forms.PrintRequestForm()
        formset = printer_forms.PrintRequestFileFormSet()
        context = {'print_request_form': print_request_form,
                   'formset': formset,
                   'sidebarSection': 'print_request_create'
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request_form = printer_forms.PrintRequestForm(request.POST)
        formset = printer_forms.PrintRequestFileFormSet(request.POST, request.FILES)
        if print_request_form.is_valid() and formset.is_valid():
            if (print_request_form.instance.description != '' or len(formset) != 0 or
                    print_request_form.instance.no_of_front_page > 0 or
                    print_request_form.instance.no_of_blank_page > 0):

                client = self.request.user
                print_request_form.instance.client = client
                print_request_form.instance.status = PrintRequest.STATUS.get_value('requested')
                print_request = print_request_form.save()
                files = list()
                for form in formset:
                    if form.instance.document:
                        form.instance.print_request = print_request
                        f = form.save()
                        files.append(f)

                subject = f'Print {client.email}'
                context = {
                    'print': print_request,
                    'files': files,
                    'request': request,
                    }
                html_message = render_to_string('printer/email/print_request_create_mail.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'ad.remoteprinter@gmail.com'
                recipient_list = [client.email]
                send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=recipient_list,
                          fail_silently=False, html_message=html_message)


                return redirect(print_request)
            else:
                messages.warning(request, "You cannot submit blank form")

        context = {'print_request_form': print_request_form,
                   'formset': formset,
                   'sidebarSection': 'print_request_create'
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

    def get_context_data(self, **kwargs):
        # pylint: disable=arguments-differ
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sidebarSection'] = 'user_print_request_list'
        return context

class UserPrintRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, View):

    template_name = 'printer/user_print_request_detail.html'

    def get(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        print_request = PrintRequest.objects.filter(Q(pk=self.kwargs.get('pk')) & Q(is_deleted=False)).first()
        print_requests_files = PrintRequestFile.objects.filter(Q(print_request=print_request.pk) &
                                                               Q(is_deleted=False))
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


class StaffPrintRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    template_name = 'printer/staff_print_request_list.html'
    model = PrintRequest
    context_object_name = 'prints'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # pylint: disable=arguments-differ
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sidebarSection'] = 'staff_print_request_list'
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
        print_requests_files = PrintRequestFile.objects.filter(Q(print_request_id=print_request.pk) &
                                                               Q(is_deleted=False))
        form = printer_forms.StaffPrintRequestForm(instance=print_request)
        if print_request:
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
        print_requests_files = PrintRequestFile.objects.filter(Q(print_request_id=print_request.pk) &
                                                               Q(is_deleted=False))
        form = printer_forms.StaffPrintRequestForm(self.request.POST, instance=print_request)
        if form.is_valid():
            form.instance.status = PrintRequest.STATUS.get_value('printed')
            price = Price.objects.latest('wef')
            form.instance.printed_on = datetime.datetime.now()
            form.instance.amount = (form.instance.no_of_bnw_page * price.bnw_page +
                                    form.instance.no_of_color_page * price.color_pages +
                                    (form.instance.no_of_page +
                                     form.instance.no_of_front_page +
                                     form.instance.no_of_blank_page) * price.page)
            form.save()
            return redirect('printer:staff_print_request_list')
        else:
            context = {'print_request': print_request,
                       'print_requests_files': print_requests_files,
                       'form': form,
                       'sidebarSection': 'staff_print_request_detail',
                      }
            return render(request, self.template_name, context)

        return HttpResponse("<h1>404</h1>")


    def test_func(self):
        if self.request.user.user_type == self.request.user.UserType.get_value("staff"):
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
