from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# class based view
from django.views.generic import View
# START OF ACCOUNT ACTIVATION LIBRARY
# current url libary
from django.contrib.sites.shortcuts import get_current_site
# encoding and decoding libraries
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
# render/converting to string libraries
from django.template.loader import render_to_string
# encoding libary
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
# getting tokens from utils.py file
from .utils import TokenGenerator,generate_token

# END OF ACCOUNT ACTIVATION LIBRARY
# START OF EMAIL SENDING LIBARIES
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
#sender email libary
from django.conf import settings
from django.core.mail import EmailMessage
# Email threading libaries
import threading
# END OF ACCOUNT  SENDING LIBARIES
# START OF PASSWORD RESET GENERATORS LIBRARIES
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
# class based email threading function for quick email sending
class EmailThread(threading.Thread):
    def __innit__(self,email_message):
        self.email_message = email_message
        threading.thread.__init__()
    #self run function   
    def run(self):
        self.email_message.send()
    
# class based activation function
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        # decoding the generated token,if succesfully clicked and activating the account
        try:
            # decoding to text format
            uid= force_text(urlsafe_base64_decode(uidb64))
            # gettingparticular user id
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            #when try condition fails
            user=None
    
        #Activating the account
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request,"Account is activated successfully")
            return redirect('/baseauthetication/login')
        # redirect incase of failure
        return render('authentication/activatefail.html')
    
# sign up function
def signup(request):
    #getting user inputs
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        #checking if passwords match
        if password != confirm_password:
            messages.warning(request,'Password dont match')
            return render (request,'authentication/signup.html')
        
        # checking if email is already taken
        try:
            if User.objects.get(username = email):
                messages.warning(request,'Email is already taken')
            return render (request,'authentication/signup.html')
        except  Exception as identifier:
            pass
        # creating new user
        user = User.objects.create_user(email,email,password)
        # START OF ACTIVATION CODE
        # making new user inactive
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        # email message
        email_subject = "Activate your account"
        #  sending email/send activation link to activation.html file
        #change the dormain to actual dormain(oremengineering.com) during production
        message = render_to_string('authentication/activate.html',{'user': user,'domain':'127.0.0.1:8000','uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':generate_token.make_token(user)})
        #sending email message link to the particular user
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[user],)
        #email thread to send email immediately/fast
        EmailThread(email_message).start()
        messages.info(request,"Activate your account by clicking the link on your email")
        return redirect('/baseauthentication/login')
    
    return render(request,'authentication/signup.html')

# login function
def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['password1']
        user = authenticate(username=username, password=userpassword)
        # logging in user
        if user is not None:
            login(request,user)
            messages.success(request,"Log in successfully")
            return render(request,'index.html')
        else:
            messages.error(request,"Something went wrong")
            return redirect('/baseauthentication/login')
  
    return render(request,'authentication/login.html')

# log out function
def handlelogout(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('/baseauthentication/login/')

#class based password reset request function
class RequestRestEmailView(View):
    # get function
    def get(self,request):
        return render(request,'authentication/request-reset-email.html')
    # password reset function
    def post(self,request):
        email = request.POST['email']
        #filtering email in database
        user = User.objects.filter(email=email)
        #checking if user exist
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset your password]'
            message = render_to_string('authentication/reset-user-password.html',{'domain':'127.0.0.1:8000','uid':urlsafe_base64_encode(force_bytes(user[0].pk)),'token':PasswordResetTokenGenerator().make_token(user[0])})
            # sending the message
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])   
            #email threading
            EmailThread(email_message).start()
            messages.info(request,'We have sent you an email with instructions on how to reset your password')
            return render(request,'authentication/request-reset-email.html')
        
#class based password reset function
class SetNewPasswordView(View):
    # getting request
    def get(self,request,uidb64,token):
        
        context = {'uidb64':uidb64,'token':token}
        # catching and displaying errors
        try:
            #dencoding
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            # checking if token-generated and password-reset-token generated matches
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"password reset link is invalid")
                return render(request,'authentication/request-reset-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request,'authentication/set-new-password.html',context)
    
    # post request function
    def post(self,request,uidb64,token):
        context = {'uidb64':uidb64,'token':token}
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        #checking if passwords match
        if password != confirm_password:
            messages.warning(request,'Password dont match')
            return render (request,'authentication/set-new-password.html',context)
        #reseting the password if condition is met
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successfully, please log in with new password")
            return redirect('/baseauthentication/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went wrong")
            return render(request,'authentication/set-new-password.html',context)
        return render(request,'authentication/set-new-password.html',context)