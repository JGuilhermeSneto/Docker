from .utils import get_system_info

def container_context(request):
    return {
        'system_info': get_system_info(),
    }

