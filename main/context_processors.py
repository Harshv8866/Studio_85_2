# main/context_processors.py

from .models import Service

def services_list(request):
    return {
        'services': Service.objects.all()
    }
