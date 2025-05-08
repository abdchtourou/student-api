from django.http import JsonResponse

def hadler404(request, exception):
    message = ("Page not found  ")
    response = JsonResponse({"error": message})
    response.status_code = 404
    return response

def hadler500(request):
    message = ("Internal server error")
    response = JsonResponse({"error": message})
    response.status_code = 500
    return response


