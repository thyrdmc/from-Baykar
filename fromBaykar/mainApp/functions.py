from django.core.paginator import Paginator
from django.http import JsonResponse

from datetime import datetime
from .models import *

def pagination(data, page_size, page_number):    
    
    if page_size == "-1":
        response_data = {
            "success": True,
            "statusCode": '200-OK',
            "message": None,
            "data": {
                'data': data,
                'page_info': {
                    'page_number': 1,  # Tüm veriler tek bir sayfa üzerinde olacak
                    'has_previous': False,
                    'has_next': False,
                    'total_pages': 1,
                    'total_items': len(data),
                }
            }
        }
    
    else:
        paginator = Paginator(data, page_size)
        
        try:
            page = paginator.page(page_number)

        except:
            response_data = {
                    "success": False,
                    "statusCode": '404-Not Found',
                    "message": "Belirtilen sayfa mevcut değil.",
                    "data" : None,
            }
            return JsonResponse(response_data, status=404)   
        
        page_data = page.object_list

        response_data = {
            "success": True,
            "statusCode": '200-OK',
            "message": None,
            "data": {
                'data':page_data, 
                'page_info': {
                    'page_number': page.number,
                    'has_previous': page.has_previous(),
                    'has_next': page.has_next(),
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                }
            }
        }

    return response_data


def calculate_time_elapsed(rental_date, pick_up_time, return_date, delivery_time):
    """
        Function that calculates the time between entered dates in hours
    """
    rental_start = datetime.combine(rental_date, pick_up_time)
    rental_end = datetime.combine(return_date, delivery_time)

    time_difference = rental_end - rental_start

    # Zaman farkını saat cinsine dönüştür
    hours_elapsed = time_difference.total_seconds() / 3600

    return hours_elapsed

def check_usable_vehicles(vehicle, rental_date, return_date):

    control_flag = False

    rentalLogs = RentalRecord.objects.filter(rental_date__lte=return_date, return_date__gte=rental_date)
    total_capacity = 1

    for rl in rentalLogs:
        total_capacity += 1

        if total_capacity > vehicle.number_of_vehicles:
            control_flag = False
            return control_flag
        
    control_flag = True
    return control_flag