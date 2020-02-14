from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
# from django.views.generic import UpdateView
from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import UserRegisterForm, UserUpdateForm


# To systematically hide all local variables of a function from error logs,
# do not provide any argument to the sensitive_variables decorator.
# To systematically hide all POST parameters of a request in error reports,
# do not provide any argument to the sensitive_post_parameters decorator.

@sensitive_post_parameters()
@sensitive_variables('username', 'form')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_type = CustomUser.UserType.get_value("client")
            form.instance.is_active = 0
            user = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f"{email} registered sucessfully. please email ad.remoteprinter@gmail.com. Submitting a request to activate your account. Remote Printer reserves the right to detain any profile in accordance with regulations.")
            return redirect(user)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


# If one of your views receives an HttpRequest object with POST parameters susceptible to
#  contain sensitive information,you may prevent the values of those parameters
# from being included in the error reports using the sensitive_post_parameters decorator

# To decorate every instance of a class-based view, you need to decorate the class definition
# itself. To do this you apply the decorator to the dispatch() method of the class.

@method_decorator(sensitive_post_parameters('username'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):


    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        #pylint: disable=unused-argument
        form = UserUpdateForm(instance=request.user)
        context = {
            'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #pylint: disable=unused-argument
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        context = {
            'form' : form,
        }
        if form.is_valid():
            form.save()
            messages.info(request, "Your Profile is updated")
            return redirect('users:profile')

        return render(request, self.template_name, context)
