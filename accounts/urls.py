from django.urls import path
from . import views


app_name = 'accounts'



urlpatterns = [
    path('login', views.login_view, name='login'),
    # login
    path('logout', views.logout_view, name='logout'),
    # logout
    path('signup', views.signup_view, name='signup'),
    # registration
    path('forgotpassword', views.forgotpassword_view, name='forgotpassword'),
    path('passwordreset/<uidb64>/<token>', views.resetpassword_view, name='resetpassword'),
    #
    path('emailsent', views.emailsent_view, name='email_sent')

]