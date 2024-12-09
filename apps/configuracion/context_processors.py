from .models import Configuracion

def obtener_config(request):
    return {'config': Configuracion.obtener_config()}
