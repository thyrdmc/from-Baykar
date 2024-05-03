from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .forms import *
from .serializers import *

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login as authlogin
from django.middleware.csrf import get_token

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.core.mail import EmailMessage


# Create your views here.


def homepage(request):
    return HttpResponse("Hello")


@csrf_exempt
def register(request):
    """
        HTTP Method : POST 
        Detail : View that allows users to register to the platform
    """
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            
            form.save()

            serializer = CreateUserSerializer(form.cleaned_data)
                
            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": "Kullanici kaydi basariyla olusturuldu.",
                "data": serializer.data, 
            }
            
            return JsonResponse(response_data, status=200)
        else:
            error_messages = [error[0] for error in form.errors.values()]

            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": error_messages[0],
                "data" : None,
            }
            return JsonResponse(response_data, status=400)

    context = {'RegistrationForm': form}
    
    
    return render(request, 'mainApp/user-registration.html', context)

@csrf_exempt
def login(request):
    """
        HTTP Method : POST 
        Detail : View that enables login to platform
    """

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = form.get_user()

            if user.is_staff:
                if user.is_superuser:
                    # Logged in User has full authority on the platform

                    user_dict = {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'is_superuser': True,
                        'is_staff': True,
                        'is_customer': False,
                    }
                
                else:
                    # Logged in user has limited authorization on the platform

                    user_dict = {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'is_superuser': False,
                        'is_staff': True,
                        'is_customer': False,
                    }

            else:
                # Logged in User can only rent IHA
                 
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_superuser': False,
                    'is_staff': False,
                    'is_customer': True,
                }

            authlogin(request, user)
            csrf_token = get_token(request)
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response_data = {
                    "success": True,
                    "statusCode": '200-OK',
                    "message": "Giris Basarili",
                    "data": {'user' : user_dict, 'access_token':access_token},
                    
            }
            return JsonResponse(response_data, status=200) 
        
        else:
            error_messages = form.get_error_message()
            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": "Lütfen kullanıcı adı ve şifre bilgilerinizi kontrol ediniz. Her iki alanın da büyük/kücük harfe duyarli olabilecegini unutmayin.",
                "data" : None,
            }

            return JsonResponse(response_data, status=400)  

    context = {'LoginForm': form}
    return render(request, 'mainApp/login.html', context)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
        HTTP Method : POST 
        Detail : Sending a password reset mail to the user
    """

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                
                # Saving Mail Log Record to Database
                MailLogs.objects.create(
                    user = user,
                    mail_type = 0,
                )

                current_site = get_current_site(request)
                mail_subject = 'Şifre Yenileme'
                message = render_to_string('mainApp/reset-password-email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'id': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                response_data = {
                    "success": True,
                    "statusCode": '200-OK',
                    "message": "Şifre sıfırlama e-postası gönderildi. Lütfen e-postanızı kontrol edin.",
                    "data": None,
                }
                return JsonResponse(response_data, status=200)
            
            else:
                response_data = {
                "success": False,
                "statusCode": '400-BadRequest',
                "message": "E-Posta adresiniz dogrulanamadi. Lutfen bilgilerinizi kontrol ediniz.",
                "data": None,
                }
                return JsonResponse(response_data, status=400)
            
            
        else:
            response_data = {
                "success": False,
                "statusCode": '400-BadRequest',
                "message": "Sunucu istenmeyen bir hata ile karşılaştı.",
                "data": None,
            }
            return JsonResponse(response_data, status=400)


    context = {'ResetPassword': form}

    return render(request, 'mainApp/forgot-password.html', context)

def reset_password_validate(request, uidb64, token):
    try:
        id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['id'] = id
        return redirect('reset_password')
    
    else:
        response_data = {
        "success": False,
        "statusCode": '400-BadRequest',
        "message": "Sifre yenileme linkinin suresi dolmustur, lutfen tekrar yenileme e-postasi aliniz.",
        "data": None,
        }
        return JsonResponse(response_data, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            id = request.POST.get('id')
            uid = urlsafe_base64_decode(id).decode()

            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 == new_password2:
                user = User.objects.get(pk=uid)
                user.set_password(new_password1)
                user.save()

                response_data = {
                    "success": True,
                    "statusCode": '200-OK',
                    "message": "Sifre degisikligi basarili bir sekilde tamamlandi",
                    "data": None, 
                }
                return JsonResponse(response_data, status=200)
            else:
                response_data = {
                "success": False,
                "statusCode": '400-BadRequest',
                "message": "Girilen sifreler ayni degildir. Lutfen tekrar deneyiniz.",
                "data": None,
                }
                return JsonResponse(response_data, status=400)
    else:
        form = SetPasswordForm(request.user)

    context = {'form': form}

    return render(request, 'mainApp/reset-password.html', context)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": "Sifre degisikligi basarili bir sekilde tamamlandi",
                "data": None, 
            }
            return JsonResponse(response_data, status=200) 
        else:
            response_data = {
                "success": False,
                "statusCode": '400-BadRequest',
                "message": "Şifre değişikliği başarısız oldu. Lutfen girilen bilgileri kontrol ediniz.",
                "errors": None,
            }
            return JsonResponse(response_data, status=400)
        
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}

    return render(request, 'accounts/change-password.html', context)

