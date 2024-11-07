# Este mixin permite definir un método que valida si el usuario cumple con ciertas condiciones antes de permitirle acceder a la vista.
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.info(request, 'No tiene permiso para acceder a este módulo.')
            return redirect('productos:dashboard')
        return super().dispatch(request, *args, **kwargs)


