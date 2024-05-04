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

import random, string

from .functions import *

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

def logout(request):
    return redirect('login')

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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_vehicle(request):
    """
        HTTP Method : POST 
        Detail : View that enables the creation of IHA 
                (approves if the user sending the request is is_staff)
    """
        
    form = VehicleForm()
    if request.method == 'POST':
        form = VehicleForm(data=request.POST)
        
        if form.is_valid():

            if request.user.is_staff:
                # For Person authorized to create IHA

                vehicle = form.save(commit=False)

                vehicle.created_by = request.user
                vehicle.usable_vehicles = form.cleaned_data['number_of_vehicles']
                vehicle.save()

                serializer = VehicleSerializer(vehicle)

                response_data = {
                    "success": True,
                    "statusCode": '200-OK',
                    "message": "IHA basarili bir sekilde olusturuldu.",
                    "data": serializer.data, 
                }

                return JsonResponse(response_data, status=200)
            
            else:
                # For Person who is not authorized to create IHA

                response_data = {
                    "success": False,
                    "statusCode": '400-Bad Request',
                    "message": "Bu islem icin yetkiniz bulunmamaktadir.",
                    "data" : None,
                }
                return JsonResponse(response_data, status=400)
        else:
            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": "Bad request",
                "data" : None,
            }
            return JsonResponse(response_data, status=400)
        
    context ={'form': form}


    return render(request, 'mainApp/vehicle-create.html', context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicles(request):    
    """
        HTTP Method : GET 
        Detail : View that enables listing of IHA's 
        Pagination : api/vehicles/?page=1&page_size=10 
                    (Each page contains 10 data, can be switched to other pages by changing the page value)
    """

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)  

    try:
        cupons = Vehicle.objects.all()
        serializer = VehicleSerializer(cupons, many=True)

    except:
        response_data = {
            "success": False,
            "statusCode": '401-Unauthorized',
            "message": "Insansiz Hava Araclarina erisilemedi.",
            "data" : None,
        }
        return JsonResponse(response_data, status=405)   

    response_data = pagination(serializer.data, page_size, page_number)

    return JsonResponse(response_data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicle(request, pk):
    """
        HTTP Method : GET 
        Detail : View that allows retrieve data of selected IHA
        Endpoint : api/vehicles/<str:pk>/
    """

    if request.method == 'GET':
        vehicle =  Vehicle.objects.filter(id=pk)
        if vehicle.exists():
            serializer = VehicleSerializer(vehicle, many=True)
            
            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": None,
                "data" : serializer.data,
            }

            return JsonResponse(response_data, status=200)   
        
        else:
            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": "Arac bilgilerine erisilemedi",
                "data" : None,
            }

            return JsonResponse(response_data, status=400) 

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_vehicle(request, pk):
    """
        HTTP Method : PUT 
        Detail : View that allows update data of selected IHA 
                (approves if the user sending the request is is_staff)
        Endpoint : api/vehicles/<str:pk>/update/
    """

    try:
        vehicle = Vehicle.objects.get(id=pk)
        number_of_vehicles = vehicle.number_of_vehicles
        
        form = VehicleForm(instance=vehicle)

    except Vehicle.DoesNotExist:
        response_data = {
            "success": False,
            "statusCode": '400-Bad Request',
            "message": "Arac bilgilerine erişilemedi",
            "data": None,
        }
        return JsonResponse(response_data, status=400)

    if request.method == 'POST' or request.method == 'PUT':
        form = VehicleForm(request.POST, instance=vehicle)

        if form.is_valid():
            difference = form.cleaned_data["number_of_vehicles"] - number_of_vehicles

            form.save()

            vehicle.usable_vehicles += difference
            vehicle.save()

            serializer = VehicleSerializer(vehicle)

            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": "Arac bilgileri guncellendi.",
                "data": serializer.data, 
            }
            
            return JsonResponse(response_data, status=200)
    
    
    context = {'form': form}

    return render(request, 'mainApp/vehicle-update.html', context)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_vehicle(request, pk):
    """
        HTTP Method : DELETE 
        Detail : View that allows delete selected IHA 
                (approves if the user sending the request is is_staff)
        Endpoint : api/vehicles/<str:pk>/update/
    """
     
    vehicle =  Vehicle.objects.get(id=pk)

    if request.method == 'DELETE':
        vehicle.delete()
        
        response_data = {
            "success": True,
            "statusCode": '200-OK',
            "message": 'Arac basarili bir sekilde silindi.',
            "data" : None,
        }

        return JsonResponse(response_data, status=200)    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rent_vehicle(request):
    """
        HTTP Method : POST 
        Detail : View that allows Customers to rent the vehicle of their choice 
                (if the user sending the request is is_staff, receive a notification to contact the manager)
    """
        
    form = RentVehicleForm()
    if request.method == 'POST':
        form = RentVehicleForm(data=request.POST)
        
        if form.is_valid():
            
            # Requesting User is a customer
            if request.user.is_staff == False:
            
                rentalRecord = form.save(commit=False)

                vehicle = form.cleaned_data['vehicle']
                rental_date = form.cleaned_data['rental_date']
                pick_up_time = form.cleaned_data['pick_up_time']
                return_date = form.cleaned_data['return_date']
                delivery_time = form.cleaned_data['delivery_time']

                # time_elapsed indicates how long the leasing process will last
                time_elapsed = calculate_time_elapsed(rental_date, pick_up_time, return_date, delivery_time)

                # Check if there is a vehicle available for rent 
                if vehicle.usable_vehicles > 0:
                    vehicle.usable_vehicles -= 1
                    vehicle.save()

                else:
                    if check_usable_vehicles(vehicle, rental_date, return_date):
                        vehicle.usable_vehicles -= 1
                        vehicle.save()
                    else:
                        response_data = {
                            "success": False,
                            "statusCode": '400-Bad Request',
                            "message": "Kiralanabilir arac bulunamamaktadir.",
                            "data" : None,
                        }
                        return JsonResponse(response_data, status=400)
                    
                rentalRecord.customer = request.user
                rentalRecord.time_elapsed = time_elapsed
                rentalRecord.save()

                serializer = RentVehicleSerializer(rentalRecord)

                response_data = {
                    "success": True,
                    "statusCode": '200-OK',
                    "message": "IHA kiralama isleminiz basarili bir sekilde gerceklesti.",
                    "data": serializer.data, 
                }

                return JsonResponse(response_data, status=200)
            
            # Staff's can't rent vehicle on their own behalf
            else:
                
                response_data = {
                    "success": False,
                    "statusCode": '400-Bad Request',
                    "message": "Personel hesabinizla kiralama islemi yapmak icin lutfen yoneticinizle iletisime geciniz.",
                    "data" : None,
                }
                return JsonResponse(response_data, status=400)
            
        # form not valid
        else:
            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": "Sunucu istenmeyen bir hata ile karsilasti",
                "data" : None,
            }
            return JsonResponse(response_data, status=400)
        
    context ={'form': form}


    return render(request, 'mainApp/vehicle-rent.html', context)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def rental_records(request):    
    """
        HTTP Method : GET 
        Detail : View that enables listing of Rental Records 
        Pagination : api/rental-records/?page=1&page_size=10 
                    (Each page contains 10 data, can be switched to other pages by changing the page value)
    """

    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)  

    try:
        cupons = RentalRecord.objects.all()
        serializer = RentVehicleSerializer(cupons, many=True)

    except:
        response_data = {
            "success": False,
            "statusCode": '401-Unauthorized',
            "message": "Kiralama kayitlarina erisilemedi.",
            "data" : None,
        }
        return JsonResponse(response_data, status=405)   

    response_data = pagination(serializer.data, page_size, page_number)

    return JsonResponse(response_data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rental_record(request, pk):
    """
        HTTP Method : GET 
        Detail : View that allows retrieve data of selected Rental Record
        Endpoint : api/rental-records/<str:pk>/
    """

    if request.method == 'GET':
        vehicle =  RentalRecord.objects.filter(id=pk)
        if vehicle.exists():
            serializer = RentVehicleSerializer(vehicle, many=True)
            
            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": None,
                "data" : serializer.data,
            }

            return JsonResponse(response_data, status=200)   
        
        else:
            response_data = {
                "success": False,
                "statusCode": '400-Bad Request',
                "message": "Kiralama kaydi bilgilerine erisilemedi",
                "data" : None,
            }

            return JsonResponse(response_data, status=400) 

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_rental_record(request, pk):
    """
        HTTP Method : PUT 
        Detail : View that allows update data of selected Rental Record
        Endpoint : api/rental-records/<str:pk>/update/
    """

    try:
        rentalRecord = RentalRecord.objects.get(id=pk)        
        form = RentVehicleForm(instance=rentalRecord)

    except Vehicle.DoesNotExist:
        response_data = {
            "success": False,
            "statusCode": '400-Bad Request',
            "message": "Kiralama kayit bilgilerine erişilemedi",
            "data": None,
        }
        return JsonResponse(response_data, status=400)

    if request.method == 'POST' or request.method == 'PUT':
        form = RentVehicleForm(request.POST, instance=rentalRecord)

        if form.is_valid():
            form.save()

            serializer = RentVehicleSerializer(rentalRecord)

            response_data = {
                "success": True,
                "statusCode": '200-OK',
                "message": "Arac bilgileri guncellendi.",
                "data": serializer.data, 
            }
            
            return JsonResponse(response_data, status=200)
    
    
    context = {'form': form}

    return render(request, 'mainApp/rental-record-update.html', context)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_rental_record(request, pk):
    """
        HTTP Method : DELETE 
        Detail : View that allows delete selected Rental Record 
        Endpoint : api/rental-records/<str:pk>/update/
    """
     
    rentalRecord =  RentalRecord.objects.get(id=pk)

    if request.method == 'DELETE':
        rentalRecord.delete()
        
        response_data = {
            "success": True,
            "statusCode": '200-OK',
            "message": 'Kiralama kaydi basarili bir sekilde silindi.',
            "data" : None,
        }

        return JsonResponse(response_data, status=200)    

