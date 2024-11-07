from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class ValidacionPermisosMixin(AccessMixin):
    permission_required = ""
    url_redirect = reverse_lazy("productos:dashboard")
    permission_denied_message = 'No tiene permiso para acceder a este módulo.'

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.get_perms()):
            messages.info(request, self.permission_denied_message)
            return redirect(self.url_redirect)
        return super().dispatch(request, *args, **kwargs)