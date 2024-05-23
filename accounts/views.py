from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import AuthenticationFormWithEmail, forgotpasswordForm, resetpasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect
from django.contrib import messages




def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # create instances of the authentication forms
            form1 = AuthenticationForm(request=request, data=request.POST)
            form2 = AuthenticationFormWithEmail(request=request, data=request.POST)
            # check if form1 (standard authentication form) is valid
            if form1.is_valid():
                username = form1.cleaned_data.get('username')
                password = form1.cleaned_data.get('password')
                # authenticate the user using the extracted username and password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')

            # check if form2 (email-based authentication form) is valid                    
            if form2.is_valid():
                username = form2.cleaned_data.get('username') # this is email!
                password = form2.cleaned_data.get('password')
                # authenticate the user using the extracted username (email) and password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                
            messages.add_message(request, messages.ERROR, 'Username or password is wrong.')

        # if the request method is not POST
        form1 = AuthenticationForm()
        form2 = AuthenticationFormWithEmail()
        context = {'form1': form1, 'form2': form2}
        return render(request, 'accounts/login.html', context)
    
    else:

        return redirect('/')



@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')


        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('/')
    

def forgotpassword_view(request):
    if request.method == 'POST':
        form = forgotpasswordForm(request.POST)
        if form.is_valid():
            # get email from the form
            email = form.cleaned_data.get('email')
            try:
                # trying to find a user with the given email
                user = User.objects.get(email=email)
                # password reset token generator
                password_reset_token = PasswordResetTokenGenerator()
                # generating a token for the user
                token = password_reset_token.make_token(user)
                # encoding the user id
                uid = urlsafe_base64_encode(force_bytes(user.id))
                
                # building the reset url
                reset_url = request.build_absolute_uri(
                    reverse('accounts:resetpassword', kwargs={'uidb64': uid, 'token': token})
                    )
                
                # email details
                subject = 'Reset Password'
                message = f'Hi {user.username}, click on this link to reset your password: {reset_url}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]   
                # sending the email
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

                return HttpResponseRedirect(reverse('accounts:email_sent'))
            
            except User.DoesNotExist:
                # pop-up error message
                messages.add_message(request, messages.ERROR, 'No user with such email exists.')
        else:
            # pop-up error message
            messages.add_message(request, messages.ERROR, 'Wrong email address!')

    # if the request method is GET
    form = forgotpasswordForm()
    context = {'form': form}
    return render(request, 'accounts/forgotpassword.html', context)


def emailsent_view(request):
    return render(request, 'accounts/emailsent.html')

def resetpassword_view(request, uidb64, token):

    try:
        # decoding the user id
        uid = force_str(urlsafe_base64_decode(uidb64))
        # finding the user with the id
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # if anything goes wrong
        user = None

    # password reset token generator
    token_generator = PasswordResetTokenGenerator()
    
    # checking if the token is valid
    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            form = resetpasswordForm(request.POST)
            if form.is_valid():
                # getting the new password and saving it to the database
                password = form.cleaned_data.get('password1')
                user.set_password(password)
                user.save()

                messages.success(request, 'Your password has been successfully reset. You can now log in with your new password.')
                # redirecting to the login page
                return HttpResponseRedirect(reverse('accounts:login'))
            else:
                messages.add_message(request, messages.ERROR, 'Passwords do not match or the password does not meet the criteria!')
                
        
        # if the request method is GET
        form = resetpasswordForm()
        context = {'form': form, 'uidb64': uidb64, 'token': token, 'validLink': True}
        return render(request, 'accounts/resetpassword.html', context)
    else:
        # if the token is invalid
        context = {'validLink': False}
        return render(request, 'accounts/resetpassword.html', context)
    


