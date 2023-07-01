from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"



from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseRedirect,HttpResponse

class DangerousLoginView(LoginView):
    '''A LoginView with no CSRF protection.'''

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_exempt)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            print("redirect_to:",redirect_to)
            if redirect_to == self.request.path:
                raise ValueError(
                    'Redirection loop for authenticated user detected. Check that '
                    'your LOGIN_REDIRECT_URL doesn\'t point to a login page.')
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

urlpatterns = [
    path('login/', DangerousLoginView.as_view(template_name='common/login.html'), name='login'),
]