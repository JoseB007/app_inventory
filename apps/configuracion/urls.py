from django.urls import path

from apps.configuracion.views import Configurar

app_name = "config"
urlpatterns = [
    path("", Configurar.as_view(), name="configuraciones"),
]