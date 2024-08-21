# user_manager.middleware.py
from .models import Domain

def get_hostname(request):
    return request.get_host().split(':')[0].lower()

def get_subdomain(request):
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]
    return subdomain

