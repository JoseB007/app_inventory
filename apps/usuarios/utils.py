import random
import string
import unicodedata
import json

from django.core.mail import send_mail

from config import settings


# Función para generar contraseñas aleatorias
def generar_password(longitud):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))


# Función para eliminar los acentos
def eliminar_acentos(cadena):
    nfkd = unicodedata.normalize('NFD', cadena)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


# Función para enviar por correo las credenciales de usuario
def enviar_email_usuario(usuario, password):
    # credenciales_usuario = {
    #     'nombre de usuario': usuario.username,
    #     'contraseña': password,
    # }
    # mensaje_email = json.dumps(credenciales_usuario)
    mensaje = f"""
    Estimado Usuario, reciba un cordial saludo.

    Los siguientes son las credenciales de su cuenta de usuario en nuestra Plataforma: 
    Usuario: {usuario.username}
    Contrasena: {password}

    Muchas gracias por su atención. Cualquier duda o comentario por favor dirigirse al siguiente correo: {settings.EMAIL_HOST_USER}'
    """
    send_mail(
        subject='Credenciales de Usuario',
        message=mensaje,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[usuario.email],
        fail_silently=False,
    )
    
    # Guardar las credenciales de usuario en texto plano
    l_usuarios = open('usuarios_contraseñas.txt', 'a')
    l_usuarios.write(f'\n{usuario.username}: {password}')
    l_usuarios.close()