from django.urls import path

from apps.views import SendMailFormView, RegisterCreateView, LoginFormView, HomeView, TextView, LogoutView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', SendMailFormView.as_view(), name='send_email'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
    path('logn/', LoginFormView.as_view(), name='login1'),
    path('home',HomeView.as_view(), name='home'),
    path('login/', RegisterCreateView.as_view(), name='login'),
    path('Text/', TextView.as_view(), name='text'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
