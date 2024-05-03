from django.core.paginator import Paginator
from django.http import JsonResponse


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

