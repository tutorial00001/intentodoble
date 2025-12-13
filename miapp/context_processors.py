# miapp/context_processors.py
from .models import Practica

def usuario_actual(request):
    user_id = request.session.get("user_id")
    if user_id:
        try:
            usuario = Practica.objects.get(id=user_id)
            return {'usuario': usuario}
        except Practica.DoesNotExist:
            return {}
    return {}
