from django.utils.timezone import localdate, make_aware

from datetime import datetime

def formatear_fecha_hora_inicio(fecha=""):
    if fecha:
        f_str = f"{fecha} 00:00:00"
    else:
        f_str = f"{localdate()} 00:00:00"

    fecha_datetime = datetime.strptime(f_str, "%Y-%m-%d %H:%M:%S")
    fecha_ini = make_aware(fecha_datetime)

    return fecha_ini

def formatear_fecha_hora_fin(fecha=""):
    if fecha:
        f_str = f"{fecha} 23:59:59"
    else:
        f_str = f"{localdate()} 23:59:59"
    
    fecha_datetime = datetime.strptime(f_str, "%Y-%m-%d %H:%M:%S")
    fecha_ini = make_aware(fecha_datetime)

    return fecha_ini